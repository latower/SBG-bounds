# On the Cardinality of Identifying Code Sets for the Soccer Ball Graph


## Prerequisites

- [miniconda](https://docs.anaconda.com/free/miniconda/index.html)
- [RoundingSat v2](https://gitlab.com/MIAOresearch/software/roundingsat/-/commit/c548e1098a81d1f57dfc31560208034253d174c1)
- [VeriPB](https://gitlab.com/MIAOresearch/software/VeriPB/-/commit/54070be168642d4b14988841d958691c39c61350)

To install the `conda` environment in which we did our experiments, go to the root directory of this repository and run:

```bash
$ conda env create -f env/sbg-bounds.yml
$ conda activate sbg-bounds
```

To install the correct versions of `VeriPB` and `RoundingSat`, first install all prerequisites as specified by the respective repositories, and then run:

```bash
$ git clone https://gitlab.com/MIAOresearch/software/VeriPB.git
$ cd VeriPB
$ git checkout 54070be168642d4b14988841d958691c39c61350
$ pip3 install --user ./
$ cd ..
$ git clone https://gitlab.com/MIAOresearch/software/roundingsat.git
$ cd roundingsat
$ git checkout c548e1098a81d1f57dfc31560208034253d174c1
$ cd build
$ cmake -DCMAKE_BUILD_TYPE=Release ..
$ make
```


## Running our scripts



Assuming that the root directory of your `VeriPB` is stored in environment variable `VERIPB_DIR` and that the root directory for your `RoundingSat` is stored in environment variable `ROUNDINGSAT_DIR`, do the following.

### Cardinality of MICS for SBG

To verify that the cardinality of the *minimum identifying code set (MICS)* of the *soccer ball graph (SBG)* is indeed equal to $10$, navigate to the `scripts/` directory and run

```bash
$ chmod +x create_and_verify_SBG_cardinality_proofs.sh
$ ./create_and_verify_SBG_cardinality_proofs.sh -r ${ROUNDINGSAT_DIR} -v ${VERIPB_DIR}
```

The expected output is the following:

```
(sbg-bounds) user@machine:/path/to/SBG-bounds/scripts$ ./create_and_verify_SBG_cardinality_proofs.sh -r ${ROUNDINGSAT_DIR} -v ${VERIPB_DIR}
--------------------------------

Network: SBG.edges
Budget: 9

Step 1: Encode the soccer ball graph (SBG.edges) into PB constraints and specify that there should be at most 9 satellites
Step 2: Use RoundingSAT to show that the resulting set of PB constraints is unsatisfiable, and write the refutation proof to a file
Step 3: Use VeriPB to verify that the proof is correct

Finished generating and verifying proof for 9 satellites on network SBG.edges.
If you did not see the warning 'WARNING:root:The provided proof did not claim contradiction', we have successfully proved that there exists no ICS of cardinality 9 for the SBG graph (SBG.edges).
Otherwise, we know that there exists an ICS of cardinality 9 for SBG graph SBG.edges.

--------------------------------

Network: SBG.edges
Budget: 10

Step 1: Encode the soccer ball graph (SBG.edges) into PB constraints and specify that there should be at most 10 satellites
Step 2: Use RoundingSAT to show that the resulting set of PB constraints is unsatisfiable, and write the refutation proof to a file
Step 3: Use VeriPB to verify that the proof is correct
WARNING:root:The provided proof did not claim contradiction.

Finished generating and verifying proof for 10 satellites on network SBG.edges.
If you did not see the warning 'WARNING:root:The provided proof did not claim contradiction', we have successfully proved that there exists no ICS of cardinality 10 for the SBG graph (SBG.edges).
Otherwise, we know that there exists an ICS of cardinality 10 for SBG graph SBG.edges.
```

All generated files can be found in the `output` and `logs` subdirectories. Specifically, the generated files are the following:

```
SBG-bounds
|   - output
|   |   - SBG.edges.b10.opb  
|   |   - SBG.edges.b10.proof  
|   |   - SBG.edges.b9.opb  
|   |   - SBG.edges.b9.proof
|   - logs
|   |   - SBG.edges.b10.encoding.log 
|   |   - SBG.edges.b10.verification.log  
|   |   - SBG.edges.b9.solving.log       
|   |   - SBG.edges.reproducibility.log
|   |   - SBG.edges.b10.solving.log   
|   |   - SBG.edges.b9.encoding.log       
|   |   - SBG.edges.b9.verification.log 
```

### Number of MICSes for SBG

To verify that there exist exactly $26$ MICSes for the SBG, navigate to the `scripts/` directory and run

```bash
$ python enumerate_solutions.py -r ${ROUNDINGSAT_DIR}
```

The expected output is the following:

```
(sbg-bounds) user@machine:/path/to/SBG-bounds/scripts$ python enumerate_solutions.py -r ${ROUNDINGSAT_DIR}
Found solution #1: ('-x1', '-x10', '-x12', '-x14', '-x15', '-x18', '-x19', '-x2', '-x21', '-x23', '-x24', '-x26', '-x27', '-x28', '-x29', '-x3', '-x30', '-x31', '-x4', '-x5', '-x7', '-x8', 'x11', 'x13', 'x16', 'x17', 'x20', 'x22', 'x25', 'x32', 'x6', 'x9').
Found solution #2: ('-x1', '-x10', '-x11', '-x12', '-x13', '-x14', '-x15', '-x16', '-x17', '-x18', '-x19', '-x20', '-x21', '-x22', '-x23', '-x24', '-x25', '-x26', '-x32', '-x7', '-x8', '-x9', 'x2', 'x27', 'x28', 'x29', 'x3', 'x30', 'x31', 'x4', 'x5', 'x6').
Found solution #3: ('-x1', '-x11', '-x12', '-x13', '-x15', '-x17', '-x18', '-x2', '-x20', '-x22', '-x23', '-x24', '-x26', '-x27', '-x3', '-x30', '-x31', '-x32', '-x4', '-x7', '-x8', '-x9', 'x10', 'x14', 'x16', 'x19', 'x21', 'x25', 'x28', 'x29', 'x5', 'x6').
Found solution #4: ('-x1', '-x10', '-x11', '-x13', '-x14', '-x15', '-x16', '-x17', '-x19', '-x2', '-x21', '-x22', '-x23', '-x25', '-x27', '-x28', '-x29', '-x30', '-x31', '-x6', '-x8', '-x9', 'x12', 'x18', 'x20', 'x24', 'x26', 'x3', 'x32', 'x4', 'x5', 'x7').
Found solution #5: ('-x10', '-x12', '-x13', '-x15', '-x17', '-x19', '-x2', '-x21', '-x23', '-x24', '-x26', '-x27', '-x28', '-x29', '-x3', '-x30', '-x32', '-x4', '-x5', '-x6', '-x7', '-x8', 'x1', 'x11', 'x14', 'x16', 'x18', 'x20', 'x22', 'x25', 'x31', 'x9').
Found solution #6: ('-x11', '-x12', '-x14', '-x16', '-x17', '-x18', '-x2', '-x20', '-x21', '-x23', '-x25', '-x27', '-x29', '-x3', '-x30', '-x31', '-x32', '-x4', '-x5', '-x6', '-x7', '-x9', 'x1', 'x10', 'x13', 'x15', 'x19', 'x22', 'x24', 'x26', 'x28', 'x8').
Found solution #7: ('-x1', '-x11', '-x13', '-x14', '-x15', '-x18', '-x19', '-x2', '-x20', '-x22', '-x23', '-x24', '-x26', '-x28', '-x29', '-x30', '-x32', '-x5', '-x6', '-x7', '-x8', '-x9', 'x10', 'x12', 'x16', 'x17', 'x21', 'x25', 'x27', 'x3', 'x31', 'x4').
Found solution #8: ('-x10', '-x12', '-x14', '-x16', '-x18', '-x19', '-x2', '-x20', '-x21', '-x23', '-x24', '-x25', '-x26', '-x29', '-x3', '-x30', '-x32', '-x4', '-x5', '-x6', '-x7', '-x8', 'x1', 'x11', 'x13', 'x15', 'x17', 'x22', 'x27', 'x28', 'x31', 'x9').
Found solution #9: ('-x1', '-x10', '-x11', '-x13', '-x14', '-x16', '-x17', '-x19', '-x2', '-x20', '-x22', '-x24', '-x25', '-x27', '-x28', '-x29', '-x3', '-x30', '-x31', '-x5', '-x6', '-x8', 'x12', 'x15', 'x18', 'x21', 'x23', 'x26', 'x32', 'x4', 'x7', 'x9').
Found solution #10: ('-x10', '-x11', '-x12', '-x14', '-x16', '-x17', '-x18', '-x19', '-x2', '-x20', '-x22', '-x23', '-x24', '-x25', '-x27', '-x3', '-x31', '-x32', '-x4', '-x5', '-x6', '-x8', 'x1', 'x13', 'x15', 'x21', 'x26', 'x28', 'x29', 'x30', 'x7', 'x9').
Found solution #11: ('-x10', '-x12', '-x14', '-x15', '-x18', '-x19', '-x2', '-x21', '-x23', '-x25', '-x26', '-x28', '-x29', '-x3', '-x30', '-x31', '-x32', '-x4', '-x5', '-x6', '-x7', '-x9', 'x1', 'x11', 'x13', 'x16', 'x17', 'x20', 'x22', 'x24', 'x27', 'x8').
Found solution #12: ('-x1', '-x10', '-x11', '-x13', '-x14', '-x15', '-x18', '-x19', '-x20', '-x22', '-x24', '-x25', '-x26', '-x27', '-x28', '-x3', '-x31', '-x32', '-x4', '-x5', '-x7', '-x9', 'x12', 'x16', 'x17', 'x2', 'x21', 'x23', 'x29', 'x30', 'x6', 'x8').
Found solution #13: ('-x1', '-x10', '-x11', '-x13', '-x15', '-x16', '-x18', '-x2', '-x20', '-x21', '-x22', '-x24', '-x25', '-x26', '-x29', '-x3', '-x30', '-x31', '-x32', '-x6', '-x7', '-x9', 'x12', 'x14', 'x17', 'x19', 'x23', 'x27', 'x28', 'x4', 'x5', 'x8').
Found solution #14: ('-x1', '-x11', '-x12', '-x14', '-x16', '-x17', '-x18', '-x2', '-x20', '-x22', '-x23', '-x25', '-x27', '-x28', '-x29', '-x30', '-x31', '-x4', '-x5', '-x6', '-x8', '-x9', 'x10', 'x13', 'x15', 'x19', 'x21', 'x24', 'x26', 'x3', 'x32', 'x7').
Found solution #15: ('-x1', '-x10', '-x12', '-x13', '-x15', '-x16', '-x17', '-x19', '-x2', '-x21', '-x22', '-x24', '-x26', '-x27', '-x28', '-x29', '-x3', '-x30', '-x31', '-x4', '-x6', '-x8', 'x11', 'x14', 'x18', 'x20', 'x23', 'x25', 'x32', 'x5', 'x7', 'x9').
Found solution #16: ('-x1', '-x11', '-x12', '-x13', '-x14', '-x16', '-x17', '-x19', '-x20', '-x21', '-x23', '-x25', '-x27', '-x28', '-x29', '-x30', '-x31', '-x5', '-x6', '-x7', '-x8', '-x9', 'x10', 'x15', 'x18', 'x2', 'x22', 'x24', 'x26', 'x3', 'x32', 'x4').
Found solution #17: ('-x10', '-x12', '-x13', '-x14', '-x16', '-x17', '-x19', '-x2', '-x20', '-x21', '-x22', '-x24', '-x25', '-x26', '-x27', '-x28', '-x3', '-x32', '-x4', '-x5', '-x6', '-x8', 'x1', 'x11', 'x15', 'x18', 'x23', 'x29', 'x30', 'x31', 'x7', 'x9').
Found solution #18: ('-x1', '-x11', '-x12', '-x13', '-x15', '-x16', '-x17', '-x18', '-x20', '-x21', '-x22', '-x24', '-x26', '-x27', '-x28', '-x29', '-x32', '-x4', '-x5', '-x6', '-x7', '-x9', 'x10', 'x14', 'x19', 'x2', 'x23', 'x25', 'x3', 'x30', 'x31', 'x8').
Found solution #19: ('-x10', '-x12', '-x14', '-x16', '-x17', '-x18', '-x2', '-x20', '-x21', '-x22', '-x23', '-x25', '-x26', '-x3', '-x30', '-x31', '-x32', '-x4', '-x5', '-x6', '-x8', '-x9', 'x1', 'x11', 'x13', 'x15', 'x19', 'x24', 'x27', 'x28', 'x29', 'x7').
Found solution #20: ('-x1', '-x10', '-x12', '-x13', '-x14', '-x15', '-x17', '-x19', '-x21', '-x23', '-x25', '-x26', '-x27', '-x28', '-x29', '-x3', '-x30', '-x31', '-x4', '-x7', '-x8', '-x9', 'x11', 'x16', 'x18', 'x2', 'x20', 'x22', 'x24', 'x32', 'x5', 'x6').
Found solution #21: ('-x10', '-x11', '-x13', '-x15', '-x16', '-x17', '-x19', '-x2', '-x21', '-x22', '-x24', '-x25', '-x27', '-x28', '-x29', '-x3', '-x31', '-x32', '-x4', '-x5', '-x6', '-x8', 'x1', 'x12', 'x14', 'x18', 'x20', 'x23', 'x26', 'x30', 'x7', 'x9').
Found solution #22: ('-x1', '-x10', '-x12', '-x14', '-x16', '-x18', '-x20', '-x21', '-x23', '-x25', '-x26', '-x27', '-x28', '-x29', '-x3', '-x30', '-x31', '-x4', '-x5', '-x6', '-x7', '-x9', 'x11', 'x13', 'x15', 'x17', 'x19', 'x2', 'x22', 'x24', 'x32', 'x8').
Found solution #23: ('-x1', '-x10', '-x11', '-x12', '-x14', '-x15', '-x16', '-x17', '-x18', '-x19', '-x21', '-x23', '-x25', '-x27', '-x28', '-x29', '-x30', '-x31', '-x4', '-x5', '-x7', '-x9', 'x13', 'x2', 'x20', 'x22', 'x24', 'x26', 'x3', 'x32', 'x6', 'x8').
Found solution #24: ('-x1', '-x10', '-x11', '-x12', '-x13', '-x15', '-x16', '-x17', '-x19', '-x2', '-x21', '-x23', '-x24', '-x25', '-x27', '-x28', '-x29', '-x3', '-x30', '-x31', '-x7', '-x8', 'x14', 'x18', 'x20', 'x22', 'x26', 'x32', 'x4', 'x5', 'x6', 'x9').
Found solution #25: ('-x10', '-x12', '-x14', '-x15', '-x16', '-x17', '-x18', '-x19', '-x2', '-x21', '-x22', '-x23', '-x24', '-x26', '-x28', '-x29', '-x3', '-x32', '-x4', '-x5', '-x6', '-x8', 'x1', 'x11', 'x13', 'x20', 'x25', 'x27', 'x30', 'x31', 'x7', 'x9').
Found solution #26: ('-x11', '-x13', '-x14', '-x16', '-x17', '-x19', '-x2', '-x20', '-x22', '-x23', '-x25', '-x27', '-x28', '-x3', '-x30', '-x31', '-x32', '-x4', '-x5', '-x6', '-x8', '-x9', 'x1', 'x10', 'x12', 'x15', 'x18', 'x21', 'x24', 'x26', 'x29', 'x7').
Current formula /path/to/SBG-bounds/output/SBG.edges.b_10.it_26.opb is unsatisfiable.
Found number of solutions: 26.
SUCCESS: Verified that /path/to/SBG-bounds/output/SBG.edges.b_10.it_26.opb is indeed unsatisfiable.
Confirmed that solution 1 is indeed a solution of /path/to/SBG-bounds/output/SBG.edges.b_10.it_00.opb.
Confirmed that solution 2 is indeed a solution of /path/to/SBG-bounds/output/SBG.edges.b_10.it_00.opb.
Confirmed that solution 3 is indeed a solution of /path/to/SBG-bounds/output/SBG.edges.b_10.it_00.opb.
Confirmed that solution 4 is indeed a solution of /path/to/SBG-bounds/output/SBG.edges.b_10.it_00.opb.
Confirmed that solution 5 is indeed a solution of /path/to/SBG-bounds/output/SBG.edges.b_10.it_00.opb.
Confirmed that solution 6 is indeed a solution of /path/to/SBG-bounds/output/SBG.edges.b_10.it_00.opb.
Confirmed that solution 7 is indeed a solution of /path/to/SBG-bounds/output/SBG.edges.b_10.it_00.opb.
Confirmed that solution 8 is indeed a solution of /path/to/SBG-bounds/output/SBG.edges.b_10.it_00.opb.
Confirmed that solution 9 is indeed a solution of /path/to/SBG-bounds/output/SBG.edges.b_10.it_00.opb.
Confirmed that solution 10 is indeed a solution of /path/to/SBG-bounds/output/SBG.edges.b_10.it_00.opb.
Confirmed that solution 11 is indeed a solution of /path/to/SBG-bounds/output/SBG.edges.b_10.it_00.opb.
Confirmed that solution 12 is indeed a solution of /path/to/SBG-bounds/output/SBG.edges.b_10.it_00.opb.
Confirmed that solution 13 is indeed a solution of /path/to/SBG-bounds/output/SBG.edges.b_10.it_00.opb.
Confirmed that solution 14 is indeed a solution of /path/to/SBG-bounds/output/SBG.edges.b_10.it_00.opb.
Confirmed that solution 15 is indeed a solution of /path/to/SBG-bounds/output/SBG.edges.b_10.it_00.opb.
Confirmed that solution 16 is indeed a solution of /path/to/SBG-bounds/output/SBG.edges.b_10.it_00.opb.
Confirmed that solution 17 is indeed a solution of /path/to/SBG-bounds/output/SBG.edges.b_10.it_00.opb.
Confirmed that solution 18 is indeed a solution of /path/to/SBG-bounds/output/SBG.edges.b_10.it_00.opb.
Confirmed that solution 19 is indeed a solution of /path/to/SBG-bounds/output/SBG.edges.b_10.it_00.opb.
Confirmed that solution 20 is indeed a solution of /path/to/SBG-bounds/output/SBG.edges.b_10.it_00.opb.
Confirmed that solution 21 is indeed a solution of /path/to/SBG-bounds/output/SBG.edges.b_10.it_00.opb.
Confirmed that solution 22 is indeed a solution of /path/to/SBG-bounds/output/SBG.edges.b_10.it_00.opb.
Confirmed that solution 23 is indeed a solution of /path/to/SBG-bounds/output/SBG.edges.b_10.it_00.opb.
Confirmed that solution 24 is indeed a solution of /path/to/SBG-bounds/output/SBG.edges.b_10.it_00.opb.
Confirmed that solution 25 is indeed a solution of /path/to/SBG-bounds/output/SBG.edges.b_10.it_00.opb.
Confirmed that solution 26 is indeed a solution of /path/to/SBG-bounds/output/SBG.edges.b_10.it_00.opb.
All found solutions are unique.
SUCCESS: verified that all found solutions are indeed solutions to the problem.
```


All generated files can be found in the `output` and `logs` subdirectories. Specifically, this script generates the following files:

```
SBG-bounds
|   - output
|   |   - SBG.edges.b_10.it_00.opb
|   |   - ...
|   |   - SBG.edges.b_10.it_26.opb
|   |   - SBG.edges.b_10.it_00.sol_01.opb
|   |   - ...
|   |   - SBG.edges.b_10.it_00.sol_26.opb
|   |   - SBG.edges.b_10.it_00.sol_01.opb.proof
|   |   - ...
|   |   - SBG.edges.b_10.it_00.sol_26.opb.proof
|   |   - SBG.edges.b_10.proof
|   - logs
|   |   - SBG.edges.b_10.it_00.encoding.log
|   |   - SBG.edges.b_10.it_00.solving.log  
|   |   - ...      
|   |   - SBG.edges.b_10.it_26.solving.log
|   |   - SBG.edges.b_10.it_26.sol_01.solving.log    
|   |   - ...      
|   |   - SBG.edges.b_10.it_26.sol_26.solving.log 
|   |   - SBG.edges.b_10.it_26.verification.log
```