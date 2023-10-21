#!/bin/bash

python 4-to-1_test.py --model_name_or_path 4-to-1_bert/ --output_json 4-to-1_bert.json --validation_file ${2} --context_file ${1}
python 4-to-1_test.py --model_name_or_path 4-to-1_hfl/ --output_json 4-to-1_hfl.json --validation_file ${2} --context_file ${1}
python 4-to-1_test.py --model_name_or_path 4-to-1_t2v/ --output_json 4-to-1_t2v.json --validation_file ${2} --context_file ${1}
python 4-to-1_voting.py
python 1-to-ans_test.py --test_file final_test.json --model_name_or_path 1-to-ans_e5b4l1_t2v --output_csv output_e5b4l1_t2v.csv
python 1-to-ans_test.py --test_file final_test.json --model_name_or_path 1-to-ans_e5b8l1_t2v --output_csv output_e5b8l1_t2v.csv
python 1-to-ans_test.py --test_file final_test.json --model_name_or_path 1-to-ans_e5b8l1_hfl --output_csv output_e5b8l1_hfl.csv
python bracket_filled.py --test_file output_e5b4l1_t2v.csv --out_file output_e5b4l1_t2v_final.csv
python bracket_filled.py --test_file output_e5b8l1_t2v.csv --out_file output_e5b8l1_t2v_final.csv
python bracket_filled.py --test_file output_e5b8l1_hfl.csv --out_file output_e5b8l1_hfl_final.csv
python 1-to-ans_voting.py --out_file ${3}
