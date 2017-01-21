CS 4410 Operating Systems Fall 2016
___


10-P2: Synchronization
=====================

**Due**: Monday, October 3

Overview
--------

The `src` directory contains several several questions.  For each question,
please modify the corresponding qXX.py file to contain the required answers and
solutions.

When a coding answer is called for, modify the skeletal code we have provided
to solve the problem, making sure your solution makes progress whenever it is
feasible to do so, and obeys the safety criteria described in the problem
description. 

Commandments
------------

All of your answers should follow the
[commandments of synchronization][commandments].

[commandments]: http://www.cs.cornell.edu/courses/cs4410/2012fa/papers/commandments.pdf

They should also guarantee safety, and make progress whenever it is possible to
do so.

The 4410 Synchronization Library
--------------------------------

Instead of using python's built-in synchronization primitives, we are using the
primitives in the provided file [rvr.py](src/rvr.py).  These primitives provide helpful
debugging output for you, and support for autograding for us.  The documentation
for this library is included in the file [doc/rvr.md](doc/rvr.md).

**Your code must not use the python Thread, Semaphore, Lock, or Condition classes**.

Updates and Clarifications
--------------------------

Any updates to this assignment (e.g. bug fixes) will be announced in pinned
posts on [Piazza](http://piazza.com/cornell/fall2016/cs4410/home).  All non-pinned
posts should be considered non-binding and advisory.

Submission
----------

Push your code to Github. You can (and realistically should) push your
code as many times as you want, such as when you have made a
significant change or improvement. Whatever code is in the repo at
midnight the night that the assignment is due will be what is graded.

