# Applied Deep Learning HW1 <br>Chinese Extractive Question Answering

### Task Description

The input for this task consists of four paragraphs and a question that we aim to answer. Initially, our objective is to identify the relevant paragraph. Subsequently, we must ascertain the starting and ending positions of the answer span. The models required for this task include a multiple-choice model and an extracted QA model. 

### How to Run

```bash
bash ./download.sh
bash ./run.sh /path/to/context.json /path/to/test.json /path/to/pred/prediction.csv
```

#### `download.sh`

Download six pre-trained models, with three dedicated to Paragraph Selection and the remaining three for Question Answering.

#### `run.sh`

Input the test data into the model and generate the predicted results. 

### Complete Training Process

#### Part 1. Paragraph Selection

##### Step 1-1 Training

```bash
$ python 4-to-1_train.py --model_name_or_path shibing624/text2vec-base-chinese --output_dir 4-to-1_t2v
$ python 4-to-1_train.py --model_name_or_path hfl/chinese-roberta-wwm-ext --output_dir 4-to-1_hfl
$ python 4-to-1_train.py --model_name_or_path bert-base-chinese --output_dir 4-to-1_bert
```

After completing this step, three models will be generated. Due to limited execution time, these three models will be downloaded using `download.sh`. 

The code is primarily modified from `run_swag_no_trainer.py` [1], with adjusted hyperparameters as follows: 

| arguments                       | value                  |
| ------------------------------- | ---------------------- |
| `--max_seq_length`              | `512`                  |
| `--model_name_or_path`          | Three different models |
| `--per_device_train_batch_size` | `2`                    |
| `--per_device_eval_batch_size`  | `1`                    |
| `--learning_rate`               | `3e-5`                 |
| `--num_train_epochs`            | `1`                    |
| `--gradient_accumulation_steps` | `2`                    |

"Besides adjusting parameters, after the `load_datasets` step, it is necessary to modify the data format of `raw_datasets["train"]` and `raw_datasets["validation"]` into a format compatible with Multiple Choice for subsequent training. The acceptable format for Multiple Choice is as follows: 

```
{'ending0', 'ending1', 'ending2', 'ending3', 'label', 'sent1', 'sent2'}
```

`ending0` - `ending3` need to be extracted from the `paragraph` using the `index` and `context.json`.

`label` is a number ranging from `0-3`, indicating which of the endings (`ending 0` - `ending3`) is the correct answer.

`sent1` represents the `question`, while `sent2` is an empty string.

Since `sent1` and `sent2` will be concatenated into the `startphrase`, having an empty string for `sent2` does not impact the training of the model."

##### Step 1-2 Testing

```bash
$ python 4-to-1_test.py --model_name_or_path 4-to-1_bert/ --output_json 4-to-1_bert.json --validation_file ${2} --context_file ${1}
$ python 4-to-1_test.py --model_name_or_path 4-to-1_hfl/ --output_json 4-to-1_hfl.json --validation_file ${2} --context_file ${1}
$ python 4-to-1_test.py --model_name_or_path 4-to-1_t2v/ --output_json 4-to-1_t2v.json --validation_file ${2} --context_file ${1}
```

After completing this step, the three recently generated models will be used to predict results and generate three corresponding JSON files.

The code is primarily modified from `4-to-1_train.py`, with the training process removed and replaced with using the just-trained models. The adjusted hyperparameters are as follows:

| arguments              | value                                                        |
| ---------------------- | ------------------------------------------------------------ |
| `--model_name_or_path` | Three different models <br>(corresponding to `output_dir` in `4-to-1_train.py`) |

Notably, the output data format needs to be modified to a format acceptable for Question Answering for subsequent training. The acceptable format for Question Answering is as follows:

```
{'answers': {'answer_start', 'text'}, 'context', 'id', 'question'}
```

Since the test data originally does not have `answers`, `answer_start = [0]`, and `text = ['']`.

`context` represents the result selected from the four candidate paragraphs after the model training.

##### Step 1-3 Voting

```bash
$ python 4-to-1_voting.py
```

This step primarily involves conducting a vote, where the model trained with `bert` takes precedence. In other words, if the results predicted by the three models are different, the result from `bert` will be considered as the answer. Conversely, if two or more models select the same answer, that answer will be deemed the final result. Upon completion, a file named `final_test.json` will be generated as the input for question answering.

#### Part 2. Question Answering

##### Step 2-1 Data Pre-processing

```bash
$ python data_for_qa.py
```

This step mainly involves converting the formats of the train data and validation data into a format compatible with question answering. 

##### Step 2-2 Training

```bash
$ python 1-to-ans_train_roberta.py --model_name_or_path hfl/chinese-roberta-wwm-ext --output_dir 1-to-ans_e5b8l1_hfl --num_train_epochs 5 --learning_rate 1e-5 --per_device_train_batch_size 8
$ python 1-to-ans_train.py --model_name_or_path shibing624/text2vec-base-chinese --output_dir 1-to-ans_e5b4l1_t2v --num_train_epochs 5 --learning_rate 1e-5 --per_device_train_batch_size 4
$ python 1-to-ans_train.py --model_name_or_path shibing624/text2vec-base-chinese --output_dir 1-to-ans_e5b8l1_t2v --num_train_epochs 5 --learning_rate 1e-5 --per_device_train_batch_size 8
```

After completing this step, three models will also be generated. Due to limited execution time, these three models will be downloaded using `download.sh`.

The code is primarily modified from the training section of `run_qa_no_trainer.py` [3], with adjusted hyperparameters as follows:

| arguments                       | value                                                        |
| ------------------------------- | ------------------------------------------------------------ |
| `--max_seq_length`              | `512`                                                        |
| `--model_name_or_path`          | `hfl/chinese-roberta-wwm-ext` or <br/>`shibing624/text2vec-base-chinese` |
| `--per_device_train_batch_size` | `4` or `8`                                                   |
| `--per_device_eval_batch_size`  | `1`                                                          |
| `--learning_rate`               | `1e-5`                                                       |
| `--num_train_epochs`            | `5`                                                          |
| `--gradient_accumulation_steps` | `4`                                                          |

##### Step 2-3 Testing

```bash
$ python 1-to-ans_test.py --test_file final_test.json --model_name_or_path 1-to-ans_e5b4l1_t2v --output_csv output_e5b4l1_t2v.csv
$ python 1-to-ans_test.py --test_file final_test.json --model_name_or_path 1-to-ans_e5b8l1_t2v --output_csv output_e5b8l1_t2v.csv
$ python 1-to-ans_test.py --test_file final_test.json --model_name_or_path 1-to-ans_e5b8l1_hfl --output_csv output_e5b8l1_hfl.csv
```

After completing this step, the three recently generated models will be used to predict results, generating three corresponding CSV files.

The code is primarily modified from the testing section of `run_qa_no_trainer.py` [3], with adjusted parameters as follows:

| arguments              | value                                                        |
| ---------------------- | ------------------------------------------------------------ |
| `--model_name_or_path` | Three different models <br/>(corresponding to `output_dir` in `1-to-ans_train.py`) |

##### Step 2-4 Data Post-processing

```bash
$ python bracket_filled.py --test_file output_e5b4l1_t2v.csv --out_file output_e5b4l1_t2v_final.csv
$ python bracket_filled.py --test_file output_e5b8l1_t2v.csv --out_file output_e5b8l1_t2v_final.csv
$ python bracket_filled.py --test_file output_e5b8l1_hfl.csv --out_file output_e5b8l1_hfl_final.csv
```

This step primarily involves converting potentially unreasonable answers into more sensible ones. For example, if the predicted result contains only a left parenthesis without a corresponding right parenthesis, the right parenthesis will be appended at the end of the answer. This adjustment helps improve accuracy to some extent. 

##### Step 2-5 Voting

```bash
$ python 1-to-ans_voting.py --out_file ${3}
```

This step mainly involves conducting a vote, with the model trained by `hfl` taking the lead. In other words, if the results predicted by the three models differ, the outcome from `hfl` will be considered as the answer. Conversely, if two or more models predict the same answer, that answer will be deemed the final result. Upon completion, the final results will be generated at the path specified in `run.sh`. 

Reference: 

[1] `run_swag_no_trainer.py` source code

https://github.com/huggingface/transformers/blob/main/examples/pytorch/multiple-choice/run_swag_no_trainer.py

[2] Multiple choice related work

https://huggingface.co/docs/transformers/tasks/multiple_choice

[3] `run_qa_no_trainer.py` source code

https://github.com/huggingface/transformers/blob/main/examples/pytorch/question-answering/run_qa_no_trainer.py

[4] Question answering related work

https://huggingface.co/docs/transformers/tasks/question_answering

Homework Spec:

https://docs.google.com/presentation/d/1EcHhZB_aBX3dGJ6odcBHvkuD6SYg5SNAvzO1soObuYY/edit#slide=id.p