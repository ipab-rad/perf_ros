# Automatic Configuration of ROS Applications for Near-Optimal Performance

This tool is a work-in-progress that allows to automatically configuring ROS applications in order to solve the following problems:

  1) Determining the specific node settings, and allocation of ROS nodes to computers that maximises the system performance. 
  2) Determining the allocation of ROS nodes to computers that minimises the hardware requirements, given specific node settings.
  
The tool is developed in python 2.7.x and is heavily used in the paper  "Automatic configuration of ROS applications for near-optimal performance" submitted to IROS 2016.


## Files description

These are the files included in the repository:

exp_greedy_1.csv: file used to run the tool (defines ten problems that will be solved by greedy_1.py)

exp_greedy_2.csv: file used to run the tool (defines ten problems that will be solved by greedy_2.py)

experiments.py  : based on the definitions in problem.py, defines the system instances (problems) to solve.

greedy_1.py     : implements the greedy heuristic that solves the problem of performance maximisation.

greedy_2.py     : implements the greedy heuristic that solves the problem of hardware resources minimistation.

model.py        : defines all classes used by the tool (Problem, Allocation, Computer, Node, Setting, Message, and Link).

problem.py      : defines the baseline problem (system instance) we want to solve, including the number of ROS nodes per type of robot, the number of servers and the their capacity. Note that when solving problem 2, SERVER_CAPACITY must be = 0.


## Running the tool

Being in the /sim directory run the following command:

  python experiments.py FILE.csv
  
  
## Further Information

For futher details of this work, please consult the paper or contact one of the following main authors:

Jose Cano: jcanore@inf.ed.ac.uk <br />
Alejandro Bordallo: alex.bordallo@ed.ac.uk

