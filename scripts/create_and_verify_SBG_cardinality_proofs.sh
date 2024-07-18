#!/bin/bash

while getopts r:v: flag
do
    case "${flag}" in
        r) ROUNDINGSAT_DIR=${OPTARG};;
        v) VERIPB_DIR=${OPTARG};;
        # f) fullname=${OPTARG};;
    esac
done

########## SETUP ##########

mkdir -p ../output
mkdir -p ../logs

this_dir="$(pwd)"

OUT_DIR="$(dirname "$this_dir")/output"
LOG_DIR="$(dirname "$this_dir")/logs"

network="SBG.edges"

########## RECORD REPRODUCIBILITY INFO ##########

project_repo="$(git config --get remote.origin.url)"
project_commit="$(git log --format=\"%H\" -n 1)"

roundingsat_repo="$(git --git-dir ${ROUNDINGSAT_DIR}/.git config --get remote.origin.url)"
roundingsat_commit="$(git --git-dir ${ROUNDINGSAT_DIR}/.git log --format=\"%H\" -n 1)"

veripb_repo="$(git --git-dir ${VERIPB_DIR}/.git config --get remote.origin.url)"
veripb_commit="$(git --git-dir ${VERIPB_DIR}/.git log --format=\"%H\" -n 1)"

python_version="$(python -V)"
networkx_version="$(conda list | grep networkx)"

repro_log_file="${LOG_DIR}/${network}.reproducibility.log"
rm ${repro_log_file}
echo "Reproducibility info" >> ${repro_log_file}
echo "====================" >> ${repro_log_file}
echo "" >> ${repro_log_file}

echo "Project" >> ${repro_log_file}
echo "-------" >> ${repro_log_file}
echo "Project repository:     ${project_repo}" >> ${repro_log_file}
echo "Project commit:         ${project_commit}" >> ${repro_log_file}
echo "" >> ${repro_log_file}

echo "RoundingSAT" >> ${repro_log_file}
echo "-----------" >> ${repro_log_file}
echo "RoundingSAT repository: ${roundingsat_repo}" >> ${repro_log_file}
echo "RoundingSAT commit:     ${roundingsat_commit}" >> ${repro_log_file}
echo "" >> ${repro_log_file}

echo "VeriPB" >> ${repro_log_file}
echo "------" >> ${repro_log_file}
echo "VeriPB repository:      ${veripb_repo}" >> ${repro_log_file}
echo "VeriPB commit:          ${veripb_commit}" >> ${repro_log_file}
echo "" >> ${repro_log_file}

echo "Other" >> ${repro_log_file}
echo "-----" >> ${repro_log_file}
echo "Python version:         ${python_version}" >> ${repro_log_file}
echo "Networkx version:       ${networkx_version}" >> ${repro_log_file}


########## Generate proof that there exists no solution with at most 9 satellites ###########

echo "--------------------------------"
echo ""

budget="9"
out_file="${network}.b${budget}"

echo "Network: ${network}"
echo "Budget: ${budget}"
echo ""


echo "Step 1: Encode the soccer ball graph (${network}) into PB constraints and specify that there should be at most ${budget} satellites"
python encode_network.py --network ../input/${network} --out_dir ${OUT_DIR} --out_file ${out_file}.opb -b ${budget} > ${LOG_DIR}/${out_file}.encoding.log

echo "Step 2: Use RoundingSAT to show that the resulting set of PB constraints is unsatisfiable, and write the refutation proof to a file"
${ROUNDINGSAT_DIR}/build/roundingsat --print-sol=1 --proof-log=${OUT_DIR}/${out_file} ${OUT_DIR}/${out_file}.opb > ${LOG_DIR}/${network}.b${budget}.solving.log

echo "Step 3: Use VeriPB to verify that the proof is correct"
veripb -v ${OUT_DIR}/${out_file}.opb ${OUT_DIR}/${out_file}.proof > ${LOG_DIR}/${out_file}.verification.log
echo ""

echo "Finished generating and verifying proof for ${budget} satellites on network ${network}."
echo "If you did not see the warning 'WARNING:root:The provided proof did not claim contradiction', we have successfully proved that there exists no ICS of cardinality ${budget} for the SBG graph (${network})."
echo "Otherwise, we know that there exists an ICS of cardinality ${budget} for SBG graph ${network}."
echo ""

# ########## Show that there exists a solution with 10 satellites ###########

echo "--------------------------------"
echo ""

budget="10"
out_file="${network}.b${budget}"

echo "Network: ${network}"
echo "Budget: ${budget}"
echo ""

echo "Step 1: Encode the soccer ball graph (${network}) into PB constraints and specify that there should be at most ${budget} satellites"
python encode_network.py --network ../input/${network} --out_dir ${OUT_DIR} --out_file ${out_file}.opb -b ${budget} > ${LOG_DIR}/${out_file}.encoding.log

echo "Step 2: Use RoundingSAT to show that the resulting set of PB constraints is unsatisfiable, and write the refutation proof to a file"
${ROUNDINGSAT_DIR}/build/roundingsat --print-sol=1 --proof-log=${OUT_DIR}/${out_file} ${OUT_DIR}/${out_file}.opb > ${LOG_DIR}/${out_file}.solving.log

echo "Step 3: Use VeriPB to verify that the proof is correct"
veripb -v ${OUT_DIR}/${out_file}.opb ${OUT_DIR}/${out_file}.proof > ${LOG_DIR}/${out_file}.verification.log
echo ""

echo "Finished generating and verifying proof for ${budget} satellites on network ${network}."
echo "If you did not see the warning 'WARNING:root:The provided proof did not claim contradiction', we have successfully proved that there exists no ICS of cardinality ${budget} for the SBG graph (${network})."
echo "Otherwise, we know that there exists an ICS of cardinality ${budget} for SBG graph ${network}."