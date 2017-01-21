from rvr import MP, MPthread
import random

# Q09:
# This program simulates the creation of chocolate chip cookies.
#
# Implement the CookieMonitor monitor below using MPlocks and
# MPcondition variables.

################################################################################
## DO NOT WRITE OR MODIFY ANY CODE ABOVE THIS LINE #############################
################################################################################

class CookieMonitor(MP):
    """
    A chocolate chip cookie is made from one chocolate and three cookie dough (each
    chocolate and cookie dough can be used in only one cookie).  A thread offers an
    ingredient by calling the appropriate method; the thread will block until
    the ingredient can be used in the cookie.
    """

    def __init__(self):
        MP.__init__(self)
        #self.debug = True
        self.chocolate_available = self.Shared("num chocolate", 0)
        self.dough_available = self.Shared("num dough", 0)
        self.lock = self.Lock("monitor lock")
        self.all_dough = self.lock.Condition("All dought has arrived")
        self.all_chocolate = self.lock.Condition("All chocolate has arrived")
        self.all_ingredients = self.lock.Condition("All ingredients have arrived")


    def chocolate_ready(self):
        """Offer a chocolate and block until this chocolate can be used to make
        a cookie."""
        with self.lock:
            self.chocolate_available.inc()

            while(self.dough_available.read() < 3):
                self.all_chocolate.wait()

            self.all_dough.signal()
            self.all_dough.signal()
            self.all_dough.signal()

            self.dough_available.dec()
            self.dough_available.dec()
            self.dough_available.dec()
            self.chocolate_available.dec()
            

    def cookie_dough_ready(self):
        """Offer a cookie dough and block until this cookie dough can be used to make a
        cookie."""
        with self.lock:
            self.dough_available.inc()

            if(self.dough_available.read() >= 3):
                self.all_chocolate.signal()
            else:
                self.all_dough.wait()

#python q09-cookies.py

################################################################################
## DO NOT WRITE OR MODIFY ANY CODE BELOW THIS LINE #############################
################################################################################

class Chocolate(MPthread):
    def __init__(self, cookie, id):
        MPthread.__init__(self, cookie, id)
        self.cookie = cookie
        self.id = id

    def run(self):
        while True:
            print "Chocolate %d ready" % self.id
            self.cookie.chocolate_ready()
            print "Chocolate %d is in the oven" % self.id
            self.delay()
            print "Chocolate %d finished baking" % self.id

class CookieDough(MPthread):
    def __init__(self, cookie, id):
        MPthread.__init__(self, cookie, id)
        self.cookie = cookie
        self.id = id

    def run(self):
        while True:
            print "CookieDough %d ready" % self.id
            self.cookie.cookie_dough_ready()
            print "CookieDough %d is in the oven" % self.id
            self.delay(0.5)
            print "CookieDough %d finished baking" % self.id

if __name__ == '__main__':
    NUM_CHOCOLATE = 5
    NUM_COOKIEDOUGH = 6

    c = CookieMonitor()

    for i in range(NUM_CHOCOLATE):
        Chocolate(c, i).start()

    for j in range(NUM_COOKIEDOUGH):
        CookieDough(c, j).start()

    c.Ready()
