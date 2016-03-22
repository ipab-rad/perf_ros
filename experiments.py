
import problem as Problem
import greedy_1 as Greedy_1
import greedy_2 as Greedy_21

import csv
import sys


###################################################################################################

# System instances
INSTANCES = [
    { 'computers': 2, 'robots': 1, 'cameras': 1},
    { 'computers': 2, 'robots': 1, 'cameras': 2},
    { 'computers': 2, 'robots': 1, 'cameras': 3},
    { 'computers': 3, 'robots': 2, 'cameras': 1},
    { 'computers': 3, 'robots': 2, 'cameras': 2},
    { 'computers': 3, 'robots': 2, 'cameras': 3},
    { 'computers': 4, 'robots': 3, 'cameras': 1},
    { 'computers': 4, 'robots': 3, 'cameras': 2},
    { 'computers': 4, 'robots': 3, 'cameras': 3},
    { 'computers': 4, 'robots': 3, 'cameras': 4}
]


###################################################################################################

def process_exp_file(exp_filename):
    
    problems = gen_all_problems()
    dump_problems(problems)
    
    with open(exp_filename, 'rU') as exp_file:
        exp_reader = csv.DictReader(exp_file)
        for row in exp_reader:
          print 'Running exp: ' + row['method'] + ' on problem: ' + row['problem']
         
          problem_no = int(row['problem'])
          if problem_no < 1:
              print "Error in input file: Problem numbers begin at 1."
              sys.exit(-1)
          problem = problems[problem_no-1]
          solution = eval(row['method'])(problem)         
          print str(solution)


###################################################################################################

def gen_all_problems():
    problems = []
    for instance in INSTANCES:
        num_computers = instance['computers']
        num_robots = instance['robots']
        num_cameras = instance['cameras']
        problem = Problem.generate(num_computers, num_robots, num_cameras)
        problems.append(problem)
    return problems


###################################################################################################


def dump_problems(problems):
    with open('detailed_problems', 'w') as detail:
        n = 0
        for problem in problems:
            n += 1
            detail.write("*** PROBLEM " + str(n) + ' ***\n')
            detail.write(str(problem))
            detail.write('\n')
            detail.flush()


###################################################################################################

def greedy_1(problem):
    res = Greedy_1.solve(problem)
    return res


###################################################################################################

def greedy_2(problem):    
    res = Greedy_1.solve(problem)
    return res


###################################################################################################

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Please provide input CSV"
        sys.exit(-1)
    print 'Reading file: ' + sys.argv[1]
    process_exp_file(sys.argv[1])





