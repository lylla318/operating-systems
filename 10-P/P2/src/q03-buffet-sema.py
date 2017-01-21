from rvr import MP, MPthread
import random

MAX_FOOD_ITEMS = 4

# Q03:
#    Complete the implementation of the BuffetRestaurant monitor below using
#    MP Semaphores.

################################################################################
## DO NOT WRITE OR MODIFY ANY CODE ABOVE THIS LINE #############################
################################################################################

class BuffetRestaurant(MP):
    """
    The manager of the restaurant decided to employ some engineers to
    design a system to reduce the amount of waste produced by the
    restaurant at the end of business hours.

    As one of those engineers, you are required to design this
    system. Ensure that the hungry customer threads don't try to get
    food when there is nothing to get. The buffet table itself can
    only hold MAX_FOOD_ITEMS so at any given time there should not be
    more than MAX_FOOD_ITEMS.

    A customer can eat any single food item that is in the buffet, but each
    food item can be eaten only once.
    """
    def __init__(self, max_food):
        MP.__init__(self)
        self.debug = True
        self.foodqueue = self.Shared("foodqueue", [])
        self.buffet_full = self.Semaphore("buffet full sema", MAX_FOOD_ITEMS)
        self.producer = self.Semaphore("buffet mutex", 1)
        self.consumer = self.Semaphore("customer mutex", 1)
        self.buffet_empty = self.Semaphore("buffet empty sema", 0)

    def cook_food(self, food_item):
        """Adds a unit of food for it to be available. food_item represents
        the food that was produced (an integer). You should keep track of
        what is being cooked."""

        self.buffet_full.procure()
        self.producer.procure()
        self.foodqueue.read().append(food_item) 
        self.producer.vacate()
        self.buffet_empty.vacate()

    def get_food(self):
        """Removes piece of food that has been cooked already, and RETURNS it."""
        
        self.buffet_empty.procure()
        self.consumer.procure()
        item = self.foodqueue.read().pop(0)
        self.consumer.vacate()
        self.buffet_full.vacate()

        return item

################################################################################
## DO NOT WRITE OR MODIFY ANY CODE BELOW THIS LINE #############################
################################################################################

class Chef(MPthread):
    def __init__(self, buffet, name, num):
        MPthread.__init__(self, buffet, num)
        self.buffet = buffet
        self.name = name
        self.food_prefix = num * 100     # assumes <= 100 food_items/chef

    def run(self):
        for i in range(5):
            food_num = self.food_prefix + i
            print(self.name + ' is trying to cook food ' + str(food_num))
            self.buffet.cook_food((self.name, food_num))
            print(self.name + ' has finished cooking food ' + str(food_num))

class HungryCustomer(MPthread):
    def __init__(self, buffet, name):
        MPthread.__init__(self, buffet, name)
        self.buffet = buffet
        self.name = name

    def run(self):
        for i in range(5):
            print(self.name + ' is trying to eat food')
            item = self.buffet.get_food()
            print(self.name + ' has finished eating food ' + str(item))

if __name__ == "__main__":
    b = BuffetRestaurant(MAX_FOOD_ITEMS)
    for i in range(3):
        Chef(b, "Chef" + str(i+1), i+1).start()
        HungryCustomer(b, "HungryCustomer" + str(i+1)).start()

    b.Ready()






