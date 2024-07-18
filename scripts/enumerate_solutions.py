# encoding: utf-8
"""
Author:              Anna L.D. Latour
Creation date:       18 July 2024
Maintainer:          Anna L.D. Latour
Contact:             a.l.d.latour@tudelft.nl
File:                enumerate_solutions.py
Description:         This script verifies that there exist 26 distinct MICSes
                     (minimum identifying code sets) for the SBG (soccer ball
                     graph) in ../input/SBG.edges. It does this by doing the
                     following:
                        1. It models the MICS problem on the SBG as a PB
                        (pseudo-Boolean) constraint formula, and specifies that
                        the cardinality of the MICS must be 10.
                        2. It then goes through a loop in which it solves the
                        set of PB constraints, then creates a new set by adding
                        a constraint that excludes the found solution, and
                        solves that new set to find a ew solution. This
                        continues until it finds no new solutions.
                        3. It verifies that the final set of PB constraints is
                        indeed unsatisfiable.
                        4. It verifies that all found solutions are unique, and
                        that all found solutions are indeed solutions to the
                        original set of PB constraints.
Version:             0.0.1
Copyright:           (C) 2024, Anna L.D. Latour
License:             MIT

Copyright (C) 2024 Anna L.D. Latour

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import argparse
import os
import re
from typing import Tuple, Any

parser = argparse.ArgumentParser()
required_args = parser.add_argument_group("Required arguments")
required_args.add_argument("--roundingsat", "-r", type=str, required=True,
                           help="Path to directory with RoundingSAT.")
args = parser.parse_args()

# Set parameters
network = "SBG.edges"
budget = 10

# Define variables for writing encoding and logs
this_dir = os.path.dirname(__file__)
INPUT_DIR = os.path.abspath(f"{this_dir}/../input")
OUT_DIR = os.path.abspath(f"{this_dir}/../output")
LOG_DIR = os.path.abspath(f"{this_dir}/../logs")
for new_dir in [OUT_DIR, LOG_DIR]:
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
out_file = f"{network}.b_{budget}"

# Where to find the 'build' subdirectory for RoundingSAT
ROUNDINGSAT_DIR = args.roundingsat

# Needed for parsing the header of PB formula files.
csts_pat = re.compile(r'\* #variable= \d+ #constraint=(?P<n_csts>\d+)\s*')


################################################################################
#                                                                              #
#                               HELPER FUNCTIONS                               #
#                                                                              #
################################################################################

def parse_roundingsat_output(roundingsat_output_file: str) -> tuple[str, ...] | tuple[Any, ...]:
    """ Parse the output of RoundingSAT to extract the found solution, then
    return a tuple with strings, such that each element of the tuple represents
    a literal that is True in the solution. Return an empty tuple if no
    solution was found by RoundingSAT.
    :param roundingsat_output_file: path to file that captured RoundingSAT's
        output.
    :return: tuple of strings, where each string represents a literal that is
        True in the found solution. Return empty tuple if no solution is found.
    """
    with open(roundingsat_output_file, 'r') as rs_file:
        for line in rs_file.readlines():
            if line.startswith('v '):
                elts = line.split()[1:]
                return tuple(sorted(elts))
    return tuple([])


def construct_blocking_constraint(solution: tuple) -> str:
    """ Given a solution to a PB formula, return a PB constraint that blocks
    that solution, such that any PB formula that includes the blocking
    constraint cannot have the input solution as a solution.
    In RoundingSAT's output format, variables that are assigned 0/False are
    represented as negative literals, while variables that are assigned 1/True
    are represented as positive literals.
    Example:
       'x': positive literal, x = 1
      '-x': negative literal, x = 0
    The blocking constraint that we construct is equivalent to:
        C := sum_{x in pos_lits} (1-x) + sum_{x in neg_lits} x => 1

    :param solution: tuple of strings, where each string represent a literal
        that is True in a solution.
    :return: a string that represents a PB constraint that blocks the found
        solution, such that any set of PB constraints that includes the
        blocking constraint, cannot have the input solution as a solution.
    """

    neg_lits = [lit for lit in solution if lit.startswith('-')]
    pos_lits = [lit for lit in solution if not lit.startswith('-')]
    lhs = [f"-1 {pl}" for pl in pos_lits] + [f"+1 {nl[1:]}" for nl in neg_lits]
    rhs = 1 - len(pos_lits)
    return f"{' '.join(lhs)} >= {rhs} ;"


def add_blocking_constraint(old_pb_formula: str, new_pb_formula: str, forbidden_solution: tuple):
    """ Take a PB formula and a solution to that formula. Write to a new file
    a copy of the PB formula, with a blocking clause that prevents the
    solution to the old formula from being solution to the new one.

    :param old_pb_formula: path to PB formula without the blocking constraint.
    :param new_pb_formula: path to PB formula with the blocking constraint.
    :param forbidden_solution: the solution that must be blocked by the
        blocking constraint (tuple of strings in which each string represents
        a literal that is True in the formula).
    """
    with open(new_pb_formula, 'w') as outfile:
        with open(old_pb_formula, 'r') as infile:
            for line in infile.readlines():
                m = re.match(csts_pat, line)
                if m is not None:
                    n_csts = int(m.group('n_csts'))
                    outfile.write(line.replace(f'#constraint= {n_csts}', f'#constraint= {n_csts+1}'))
                else:
                    outfile.write(line)
        outfile.write("\n" + construct_blocking_constraint(forbidden_solution))


def add_unit_clauses(old_pb_formula: str, new_pb_formula: str, solution: tuple):
    """ Take a PB formula and a solution, and write a new PB formula to file
    that consists of the old PB formula and a set of unit clauses that specify
    that the literals that are made true by the input solution must be made
    true in the formula.

    :param old_pb_formula: path to PB formula without the unit clauses.
    :param new_pb_formula: path to PB formula with the unit clauses.
    :param solution: the solution that must be encoded by the unit clauses
        (a tuple of strings where each string represents a literal that is True
        in the formula).
    """
    with open(new_pb_formula, 'w') as outfile:
        with open(old_pb_formula, 'r') as infile:
            for line in infile.readlines():
                m = re.match(csts_pat, line)
                if m is not None:
                    n_csts = int(m.group('n_csts'))
                    outfile.write(line.replace(f'#constraint= {n_csts}', f'#constraint= {n_csts+len(solution)}'))
                else:
                    outfile.write(line)
        for lit in solution:
            if lit.startswith('-'):
                outfile.write(f"\n+1 {lit[1:]} = 0 ;")
            else:
                outfile.write(f"\n+1 {lit} = 1 ;")


def verification_successful(verification_log: str) -> bool:
    """ Parse the output of veripb to determine whether the refutation proof
    was verified successfully.
    :param verification_log: path to veripb output.
    :return: True if the verification was successful, False if not.
    """
    with open(verification_log, 'r') as logfile:
        for line in logfile.readlines():
            if "Verification succeeded." in line:
                return True
    return False


################################################################################
#                                                                              #
#                                   MAIN LOOP                                  #
#                                                                              #
################################################################################

################################################################################
# STEP 1: Encode the problem into PB constraints                               #
################################################################################
original_formula = f"{out_file}.opb"
encoding_log = f"{out_file}.encoding.log"
cmd = "python encode_network.py " + \
      f"--network {INPUT_DIR}/{network} " + \
      f"--out_dir {OUT_DIR} " + \
      f"--out_file {out_file}.it_00.opb " + \
      f"-b {budget} " + \
      f"> {LOG_DIR}/{out_file}.it_00.encoding.log"
os.system(cmd)


################################################################################
# STEP 2: Enumerate all solutions                                              #
################################################################################

satisfiable = True
it = 0
new_formula = f"{OUT_DIR}/{out_file}.it_{it:02}.opb"
unsat_formula = ""
all_solutions = []

while satisfiable:
    current_formula = new_formula
    cmd = f"{ROUNDINGSAT_DIR}/build/roundingsat " +\
          f"--print-sol=1 " + \
          f"--proof-log={OUT_DIR}/{out_file} " +\
          f"{current_formula} > " +\
          f"{LOG_DIR}/{network}.b_{budget}.it_{it:02}.solving.log"
    os.system(cmd)
    new_sol = parse_roundingsat_output(f"{LOG_DIR}/{network}.b_{budget}.it_{it:02}.solving.log")
    if not new_sol:
        satisfiable = False
        unsat_formula = current_formula
        print(f"Current formula {current_formula} is unsatisfiable.")
        print(f"Found number of solutions: {it}.")
    else:
        print(f"Found solution #{it + 1}: {new_sol}.")
        all_solutions.append(new_sol)
        new_formula = f"{OUT_DIR}/{out_file}.it_{it+1:02}.opb"
        add_blocking_constraint(current_formula, new_formula, new_sol)
        it += 1


################################################################################
# STEP 3: Verify that the current formula is unsatisfiable                     #
################################################################################

# Step 3: Use VeriPB to verify that the proof is correct
verification_log_file = f"{LOG_DIR}/{network}.b_{budget}.it_{it:02}.verification.log"
cmd = f"veripb " +\
      f"-v {unsat_formula} " +\
      f"{OUT_DIR}/{out_file}.proof " +\
      f"> {verification_log_file}"
os.system(cmd)
if verification_successful(verification_log_file):
    print(f"SUCCESS: Verified that {unsat_formula} is indeed unsatisfiable.")
else:
    raise Exception(
        f"ERROR: Unable to verify that {unsat_formula} is unsatisfiable.")

################################################################################
# STEP 4: Verify that all found solutions are indeed solutions and unique.     #
################################################################################
# We do this by adding unit clauses to the original formula; one unit clause per
# literal in the solution, then checking if the result is satisfiable.
for i, solution in enumerate(all_solutions):
    original_formula = f"{OUT_DIR}/{out_file}.it_00.opb"
    new_formula = f"{OUT_DIR}/{out_file}.it_00.sol_{i+1:02}.opb"
    add_unit_clauses(original_formula,
                     new_formula,
                     solution)
    cmd = f"{ROUNDINGSAT_DIR}/build/roundingsat " +\
          f"--print-sol=1 " + \
          f"--proof-log={OUT_DIR}/{out_file}.it_00.sol_{i+1:02}.opb " +\
          f"{new_formula} > " +\
          f"{LOG_DIR}/{network}.b_{budget}.it_{it:02}.sol_{i+1:02}.solving.log"
    os.system(cmd)
    new_sol = parse_roundingsat_output(f"{LOG_DIR}/{network}.b_{budget}.it_{it:02}.sol_{i+1:02}.solving.log")
    if not new_sol:
        satisfiable = False
        raise Exception(f"Solution {i+1} is not a solution of {original_formula}! Solution: {', '.join(solution)}, {new_sol}")
    elif new_sol == solution:
        print(f"Confirmed that solution {i+1} is indeed a solution of {original_formula}.")


# Check that all found solutions are unique:
if len(set(all_solutions)) == len(all_solutions):
    print("All found solutions are unique.")

print(f"SUCCESS: verified that all found solutions are indeed solutions to the problem.")



