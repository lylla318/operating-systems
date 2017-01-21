from rvr import MP, MPthread

# Q01:
# a. Run the following concurrent program. Try running it by itself and then 
#    try running it while browsing the web.
#    Which of the following is true? (Answer all that apply.)
#       A. The output of the program is always letter-by-letter the same.
#       B. Two outputs of the program could never be identical.
#       C. The outputs vary in an unpredictable way.
#
#       Answers B and C are true. 
#
# b. In general, when the code itself enforces no order of events, can
#    one rely on a particular timing/interleaving of executions of
#    concurrent threads?  
#       A. Yes 
#       B. No
#
#       No (B.)
#
# c. If there were a specific interleaving of threads that would be problematic,
#    how many times would you have to run this program in order to observe that
#    problematic interleaving?
#       A. 10 times
#       B. 100 times
#       C. 1000 times
#       D. You cannot guarantee that you will observe any specific interleaving 
#         of threads no matter how many times you run the code.
#
#       Answer D.
#
# d. What does this imply about the effectiveness of testing as a way to find 
#    synchronization errors?
#       A. Running the code repeatedly is a good way to test whether your code is correct.
#       B. To convince yourself that your code is correct, you must reason about 
#         the code instead of the observed outputs.
#
#       Answer B.
#

class Worker1(MPthread):
    def __init__(self, mp):
        MPthread.__init__(self, mp, "Worker 1")

    def run(self):
        while True:
            print("Hello from Worker 1")

class Worker2(MPthread):
    def __init__(self, mp):
        MPthread.__init__(self, mp, "Worker 2")

    def run(self):
        while True:
            print("Hello from Worker 2")
mp = MP()
w1 = Worker1(mp)
w2 = Worker2(mp)
w1.start()
w2.start()
