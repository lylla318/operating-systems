from rvr import MP, MPthread

# Q05:
# You are in charge of track assignemnts at Grand Central Station.
#
# The station has many tracks that a variety of trains use for loading and
# unloading passengers. For simplicity, we assume that all tracks can be used
# by any type of train: Amtrak, Metro-North, or Subway. Since both New Yorkers
# and politicians can be quite finicky, there are many regulations regarding
# how the tracks can be assigned to trains of each type. Additionally, since
# Grand Central Station is up and running almost 24/7, inpsectors must
# also be given access to the tracks. For simplicity, inspectors are
# treated as "trains" in the scheudling system.
#
# The rules are thus:
#
#   (a) There are no more than N tracks assigned to trains at any given time
#   (b) A Subway train may not begin to use a track if it would cause more than
#       80% of the tracks in use to be assigned to Subway trains
#   (c) Amtrak trains may not use a track if there are any Metro-North trains
#       currently at the station
#   (d) Likewise, Metro-North trains may not use a track if there are any Amtrak
#       trains currently at the station (The two lines compete for some of the
#       same customers, and refuse to share the station at any time, out of spite)
#   (e) Maintenance crews are always allowed priority access to the tracks
#       (subject to condition a).  No train should be allowed to use a track if
#       an inspector is waiting.
#
# The regulations make no guarantees about starvation.

# Implement the track assignement dispatcher monitor using MPlocks and
# MPcondition variables

################################################################################
## DO NOT WRITE OR MODIFY ANY CODE ABOVE THIS LINE #############################
################################################################################

class Dispatcher(MP):
    def __init__(self, n):
        MP.__init__(self, None)
        #self.debug = True
        self.num_trains = self.Shared("numtrains", 0)
        self.num_subway = self.Shared("numSubway", 0)
        self.num_amtrack = self.Shared("numAmtrack", 0)
        self.num_metronorth = self.Shared("numMetroNorth", 0)
        self.num_inspector_waiting = self.Shared("numInspectorWaiting", 0)
        self.max_trains = self.Shared("maxtrains", 15)
        self.station_lock  = self.Lock("station lock")
        self.not_full   = self.station_lock.Condition("tracks are not full")
        self.subway_not_80 = self.station_lock.Condition("less than 80 percent of tracks are assigned to subways")
        self.no_amtracks = self.station_lock.Condition("there no Amtracks in the station")
        self.no_metronorth = self.station_lock.Condition("there no MetroNorths in the station")
        self.no_inspectors_waiting = self.station_lock.Condition("there are no inspectors waiting")

    #python q05-grandcentral.py

    def subway_enter(self):
        with self.station_lock:
            while( (self.num_inspector_waiting.read() > 0) or 
                (self.num_trains.read() >= self.max_trains.read()) or    
                (self.num_trains.read() == 0) or    
                ( (self.num_trains.read() == 0) and  ( ( (self.num_subway.read()+1) / (self.num_trains.read()+1) ) > 0.8) ) ):
                if(self.num_trains.read() == 0): #prevent division by 0
                    self.subway_not_80.wait()
                if(((self.num_subway.read()+1) / (self.num_trains.read()+1)) > 0.8): #check 80% condition
                    self.subway_not_80.wait()
                if(self.num_inspector_waiting.read() > 0):
                    self.no_inspectors_waiting.wait()
                if(self.num_trains.read() >= self.max_trains.read()): #check to see if station is full
                   self.not_full.wait()
            self.num_subway.inc()
            self.num_trains.inc()

    def subway_leave(self):
        with self.station_lock:
            self.num_trains.dec()
            self.num_subway.dec()
            if(self.num_trains.read() > 0):
                if((self.num_subway.read() / self.num_trains.read()) <= 0.8):
                    self.subway_not_80.broadcast()
            self.not_full.broadcast()


    def amtrak_enter(self):
        with self.station_lock:
            while( (self.num_trains.read() >= self.max_trains.read()) or
                (self.num_inspector_waiting.read() > 0) or
                (self.num_metronorth.read() > 0) ):
                if(self.num_trains.read() >= self.max_trains.read()): #check to see if station is full
                   self.not_full.wait()
                if(self.num_inspector_waiting.read() > 0):
                    self.no_inspectors_waiting.wait()
                if(self.num_metronorth.read() > 0):
                    self.no_metronorth.wait()
            self.num_amtrack.inc()
            self.num_trains.inc()
            if(((self.num_subway.read()+1) / (self.num_trains.read()+1)) <= 0.8): #check 80% condition
                self.subway_not_80.broadcast()

    def amtrak_leave(self):
        with self.station_lock:
            self.num_trains.dec()
            self.num_amtrack.dec()
            if(self.num_amtrack.read() == 0):
               self.no_amtracks.broadcast()
            self.not_full.broadcast()
            

    def metronorth_enter(self):
        with self.station_lock:
            while( (self.num_trains.read() == self.max_trains.read()) or
                    (self.num_amtrack.read() > 0) or
                    (self.num_inspector_waiting.read() > 0) ):
                if(self.num_trains.read() == self.max_trains.read()): #check to see if station is full
                   self.not_full.wait()
                if(self.num_amtrack.read() > 0):
                    self.no_amtracks.wait()
                if(self.num_inspector_waiting.read() > 0):
                    self.no_inspectors_waiting.wait()
            self.num_trains.inc()
            self.num_metronorth.inc()
            if(((self.num_subway.read()+1) / (self.num_trains.read()+1)) <= 0.8): #check 80% condition
                self.subway_not_80.broadcast()

    def metronorth_leave(self):
        with self.station_lock:
            self.num_trains.dec()
            self.num_metronorth.dec()
            if(self.num_metronorth.read() == 0):
                self.no_metronorth.broadcast()
            self.not_full.broadcast()

    def inspector_enter(self):
        with self.station_lock:
            self.num_inspector_waiting.inc()
            while(self.num_trains.read() == self.max_trains.read()): #check to see if station is full
               self.not_full.wait()
            self.num_trains.inc()
            self.num_inspector_waiting.dec()
            if(self.num_inspector_waiting.read() == 0):
                self.no_inspectors_waiting.broadcast()
            if(((self.num_subway.read()+1) / (self.num_trains.read()+1)) <= 0.8): #check 80% condition
                self.subway_not_80.broadcast()

    def inspector_leave(self):
        with self.station_lock:
            self.num_trains.dec()
            self.not_full.broadcast()

################################################################################
## DO NOT WRITE OR MODIFY ANY CODE BELOW THIS LINE #############################
################################################################################

SUBWAY      = 0
AMTRACK     = 1
METRONORTH  = 2
INSPECTOR   = 3

class Train(MPthread):
    def __init__(self, train_type, dispatcher, name):
        MPthread.__init__(self, dispatcher, name)
        self.train_type = train_type
        self.dispatcher = dispatcher

    def run(self):
        enters = [self.dispatcher.subway_enter,
                  self.dispatcher.amtrak_enter,
                  self.dispatcher.metronorth_enter,
                  self.dispatcher.inspector_enter]
        leaves = [self.dispatcher.subway_leave,
                  self.dispatcher.amtrak_leave,
                  self.dispatcher.metronorth_leave,
                  self.dispatcher.inspector_leave]
        names  = ['subway', 'amtrak', 'metro north', 'inspector']

        print("%s train trying to arrive" % names[self.train_type])
        enters[self.train_type]()
        print("%s train admitted" % names[self.train_type])
        self.delay(0.1)
        print("%s train leaving" % names[self.train_type])
        leaves[self.train_type]()
        print("%s train done" % names[self.train_type])

max_trains = 15
numbers = [10, 35, 2, 4]
dispatcher = Dispatcher(max_trains)
for t in [SUBWAY, AMTRACK, METRONORTH, INSPECTOR]:
    for i in range(numbers[t]):
        if t == 0:
            Train(t, dispatcher, 'SUBWAY' + str(i)).start()
        elif t == 1:
            Train(t, dispatcher, 'AMTRACK' + str(i)).start()
        elif t == 2:
            Train(t, dispatcher, 'METRONORTH' + str(i)).start()
        else:
            Train(t, dispatcher, 'INSPECTOR' + str(i)).start()

dispatcher.Ready()




