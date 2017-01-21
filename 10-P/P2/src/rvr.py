
# Author Robbert van Renesse, November 2015

# see the file doc/rvr.md for documentation on this package

from threading import Thread, Lock, Condition, Semaphore
from Queue import Queue
import time, threading

class Shared:
    def __init__(self, mp, name, val):
        self.mp = mp
        self.lock = Lock()
        self.name = name
        self.val = val

    def read(self):
        with self.lock:
            if self.mp.debug:
                print "thread", threading.current_thread().name, "reading", self.name, "-->", self.val
            return self.val

    def write(self, val):
        with self.lock:
            if self.mp.debug:
                print "thread", threading.current_thread().name, "writing", self.name, ":", self.val, "-->", val
            self.val = val

    def tas(self, oldval, newval):
        with self.lock:
            oldval = self.val
            self.val = True
            return oldval

    def cas(self, oldval, newval):
        with self.lock:
            if self.val == oldval:
                self.val = newval
                return True
            else:
                return False

    # *NON*-atomic increment: does a read and a write.
    def inc(self, amt=1):
        self.write(self.read() + amt)

    # *NON*-atomic decrement: does a read and a write.
    def dec(self, amt=1):
        self.write(self.read() - amt)

class MPcondition:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.cond = Condition(parent.lock)

    def wait(self):
        if self.parent.mp.debug:
            print "thread", threading.current_thread().name, "starts waiting for", self.parent.name, "/", self.name
        self.cond.wait()
        if self.parent.mp.debug:
            print "thread", threading.current_thread().name, "resuming after", self.parent.name, "/", self.name

    def signal(self):
        if self.parent.mp.debug:
            print "thread", threading.current_thread().name, "signaling", self.parent.name, "/", self.name
        self.cond.notify()

    def broadcast(self):
        if self.parent.mp.debug:
            print "thread", threading.current_thread().name, "broadcasting", self.parent.name, "/", self.name
        self.cond.notifyAll()

class MPlock:
    def __init__(self, mp, name):
        self.mp = mp
        self.name = name
        self.lock = Lock()

    def Condition(self, name):
        return MPcondition(name, self)

    def acquire(self):
        self.lock.acquire()
        if self.mp.debug:
            print "thread", threading.current_thread().name, "acquired lock", self.name

    def release(self):
        if self.mp.debug:
            print "thread", threading.current_thread().name, "releasing lock", self.name
        self.lock.release()

    def __enter__(self):
        self.acquire()

    def __exit__(self, type, value, traceback):
        self.release()

class MPsema:
    def __init__(self, mp, name, value):
        self.mp = mp
        self.name = name
        self.sema = Semaphore(value)

    def procure(self):
        self.sema.acquire()
        if self.mp.debug:
            print "thread", threading.current_thread().name, "procured", self.name

    def vacate(self):
        if self.mp.debug:
            print "thread", threading.current_thread().name, "vacating", self.name
        self.sema.release()

class MP:
    def __init__(self, seed=None):
        self.debug = False
        self.threads = Queue()

    def Lock(self, name):
        return MPlock(self, name)

    def Semaphore(self, name, value):
        return MPsema(self, name, value)

    def Shared(self, name, val):
        return Shared(self, name, val)

    def Ready(self):
        while not self.threads.empty():
            thr = self.threads.get()
            thr.join()

    def Check(self):
        pass

class MPthread(Thread):
    def __init__(self, mp, name):
        Thread.__init__(self, name=name)
        self.MP = mp
        mp.threads.put(self)

    def delay(self, amt=1):
        time.sleep(amt)

    def run(self):
        if self.MP.debug:
            print self.name, "starting"
        self.go()
        if self.MP.debug:
            print self.name, "finished"

    def MP_check(self):
        self.MP.Check()
