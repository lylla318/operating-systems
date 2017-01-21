import argparse
from rvr import MP, MPthread
import time
import sys
import random
from subprocess import Popen

################################################################################
## sequential implementation ###################################################
################################################################################

def run_sequential(N):
    """perform N steps sequentially"""
    return do_steps(0,1,N)

################################################################################
## threaded implementation #####################################################
################################################################################

class ThreadedWorker(MPthread):
    def __init__(self,mp,k,n,N):
        """initialize this thread to be the kth of n worker threads"""
        MPthread.__init__(self, mp, "Threaded Worker")
        self.k      = k
        self.n      = n
        self.N      = N
        self.result = None

    def run(self):
        """execute the worker thread's work"""
        self.result = do_steps(self.k, self.n, self.N)

def run_threaded(num_threads, N):
    """use num_thread threads to perform N steps of work"""
    mp = MP()
    threads = [ThreadedWorker(mp, i, num_threads, N)
               for i in range(num_threads)]
    for t in threads:
        t.start()
    mp.Ready()
    return sum([t.result for t in threads])

################################################################################
## multiprocess implementation #################################################
################################################################################

def run_parent(num_threads, N):
    """use num_children subprocesses to perform N steps of work"""
    children = [Popen([sys.executable, sys.argv[0], sys.argv[1], 'child', str(k), str(num_threads)])
                for k in range(num_threads)]
    return sum(child.wait() for child in children)

def run_child(N, args):
    """do the work of a single subprocess using do_steps"""
    return do_steps(int(args[0]), int(args[1]), N)

################################################################################
## unit of work ################################################################
################################################################################

def do_step_cpu(i):
    """simulates a task that requires some processing"""
    total_val = 0
    random.seed(i)
    for j in range(10000):
        total_val += random.gauss(0,2)
    if total_val / float(10000) > 0:
        return 1        
    else:
        return 0

def do_step_io(i):
    """simulates a task that requires a bit of processing and some I/O"""
    time.sleep(0.01)
    random.seed(i)
    val = random.gauss(0,2)
    if (val > 1):
        return 1
    else:
        return 0

# do_step will be set to either do_step_cpu or do_step_io
do_step = None

def do_steps(k, n, N):
    """given N units of work divided into n batches, performs the kth batch (k is
     in the range [kN/n,(k+1)N/n)."""
    start = k * N/n
    finish = min((k+1) * N/n, N)
    value = 0
    for i in range(start,finish):
        value += do_step(i)
    return value

################################################################################
## program main function #######################################################
################################################################################

# Argument parsing
def parse_args():
    parser = argparse.ArgumentParser(description="Simulates a number of CPU or IO bound tasks.")
    parser.add_argument('task_type', help="The type of task to run.",
                        type=str, choices=["cpu", "io"])
    subparsers    = parser.add_subparsers(dest='command', help="How to run the tasks.")

    seq_parser    = subparsers.add_parser("sequential")

    thread_parser = subparsers.add_parser("threaded")
    thread_parser.add_argument('num_threads', help="Number of threads to run.", type=int)

    fork_parser   = subparsers.add_parser("forked")
    fork_parser.add_argument('num_processes', help="Number of processes to run.", type=int)

    child_parser  = subparsers.add_parser("child")
    child_parser.add_argument('other', help="Your arguments go here.", nargs='*')

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    """parse the command line, execute the program, and print out elapsed time"""
    N = 100
    args = parse_args()

    if args.task_type == "cpu":
        do_step = do_step_cpu
    elif args.task_type == "io":
        do_step = do_step_io
    else:
        sys.exit(1)

    command = args.command
    start_time = time.time()

    if command == "sequential":
        print run_sequential(N)
    elif command == "threaded":
        print run_threaded(args.num_threads, N)
    elif command == "forked":
        print run_parent(args.num_processes, N)
    elif command == "child":
        # Note: this is an abuse of the exit status indication
        sys.exit(run_child(N, args.other))
    else:
        sys.exit(1)

    print "elapsed time: ", time.time() - start_time
