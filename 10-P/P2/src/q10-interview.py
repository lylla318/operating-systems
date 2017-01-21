from rvr import MP, MPthread
import random

# Q10:
#
# A group of Computer Science students wants to practice their technical
# interview skills by conducting mock interviews on each other. A coordinator
# thread will choose two students at random to pair off and interview each
# other.
#
# A student can only participate in one interview at a time.
#
# Modify the following code to avoid deadlocks.

################################################################################
## DO NOT WRITE OR MODIFY ANY CODE ABOVE THIS LINE #############################
################################################################################

mp = MP()

# students are represented by Lock objects; if a student is busy interviewing
# then the lock is held.
students = [mp.Lock(str(i)) for i in range(100)]

class Coordinator(MPthread):
    def __init__(self, id, mp):
        MPthread.__init__(self, mp, 'Coordinator')
        self.id = id

    def run(self):
        while True:
            b1 = random.randrange(100)
            b2 = random.randrange(100)

            # you can't interview yourself
            if b1 == b2:
                continue

            # standardize lock ordering
            if b1 < b2:
                temp = b1
                b1 = b2
                b2 = temp

            students[b1].acquire()
            students[b2].acquire()

            # conduct mock interview
            print ("coordinator %i matching students %i and %i" % (self.id, b1, b2))
            self.delay(0.1)

            students[b1].release()
            students[b2].release()
            

################################################################################
## DO NOT WRITE OR MODIFY ANY CODE BELOW THIS LINE #############################
################################################################################

for i in range(20):
    Coordinator(i, mp).start()
