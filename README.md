# ADL HW1 Chinese Extractive Question Answering

## 執行流程

### Part 1. Paragraph Selection

#### Step 1-1 Training

```bash
$ python 4-to-1_train.py --model_name_or_path shibing624/text2vec-base-chinese --output_dir 4-to-1_t2v
$ python 4-to-1_train.py --model_name_or_path hfl/chinese-roberta-wwm-ext --output_dir 4-to-1_hfl
$ python 4-to-1_train.py --model_name_or_path bert-base-chinese --output_dir 4-to-1_bert
```

這步完成之後會生成三個 model，因為執行時間有限，所以這三個 model 會透過 `download.sh` 下載。

程式碼主要是從 `run_swag_no_trainer.py` [1] 做修改，有做調整的 hyper parameter 如下：

| arguments                       | value           |
| ------------------------------- | --------------- |
| `--max_seq_length`              | `512`           |
| `--model_name_or_path`          | 三個 model 不同 |
| `--per_device_train_batch_size` | `2`             |
| `--per_device_eval_batch_size`  | `1`             |
| `--learning_rate`               | `3e-5`          |
| `--num_train_epochs`            | `1`             |
| `--gradient_accumulation_steps` | `2`             |

除了調整參數之外，在`load_datasets`之後，還需要將`raw_datasets["train"]`和`raw_datasets["validation"]`的資料格式改成 Multiple choice 能夠接受的格式，才能進行後續的訓練。Multiple choice 可接受的格式如下：

```
{'ending0', 'ending1', 'ending2', 'ending3', 'label', 'sent1', 'sent2'}
```

`ending0` - `ending3` 需要從 `paragraph` 的 `index` 以及 `context.json` 拿取。

`label` 為 `0-3` 的數，表示答案為 `ending 0` - `ending3` 中的哪一個。

`sent1` 為 `question`，`sent2` 為空字串。

因為`sent1`和`sent2`最後會接在一起變成`startphrase`，所以`sent2`是空字串並不影響訓練模型。

#### Step 1-2 Testing

```bash
$ python 4-to-1_test.py --model_name_or_path 4-to-1_bert/ --output_json 4-to-1_bert.json --validation_file ${2} --context_file ${1}
$ python 4-to-1_test.py --model_name_or_path 4-to-1_hfl/ --output_json 4-to-1_hfl.json --validation_file ${2} --context_file ${1}
$ python 4-to-1_test.py --model_name_or_path 4-to-1_t2v/ --output_json 4-to-1_t2v.json --validation_file ${2} --context_file ${1}
```

這步完成之後會用剛剛生成的三個 model 預測結果，並產生三個相對應的 json file。

程式碼主要是從 `4-to-1_train.py`做修改，只是將訓練的過程刪除，改成用剛剛訓練好的模型進行訓練。有做調整的 hyper parameter 如下：

| arguments              | value                                                       |
| ---------------------- | ----------------------------------------------------------- |
| `--model_name_or_path` | 三個 model 不一樣（對應 `4-to-1_train.py` 的 `output_dir`） |

特別的是，輸出的資料格式要改成 Question answering 能夠接受的格式，才能進行後續的訓練。Question answering 可接受的格式如下：

```
{'answers': {'answer_start', 'text'}, 'context', 'id', 'question'}
```

因為要拿來測試的資料本來就沒有`answers`，所以`answer_start = [0]`，`text = ['']`。

`context` 為經過模型訓練後，從四個候選段落選擇出來的結果。

#### Step 1-3 Voting

```bash
$ python 4-to-1_voting.py
```

這步主要是在做投票，這裡會以 `bert` 訓練出來的模型為主，也就是說如果三種模型預測的結果都不一樣，則會以 `bert` 的結果當作答案。反之，如果有兩個以上的模型選擇同一個答案，就會以該答案為最終結果。完成之後會產生`final_test.json` 這個檔案作為 question answering 的輸入。

### Part 2. Question Answering

#### Step 2-1 Data Pre-processing

```bash
$ python data_for_qa.py
```

這步主要是將 train data 和 validation data 的格式轉換成 question answering 能夠接受的格式。

#### Step 2-2 Training

```bash
$ python 1-to-ans_train_roberta.py --model_name_or_path hfl/chinese-roberta-wwm-ext --output_dir 1-to-ans_e5b8l1_hfl --num_train_epochs 5 --learning_rate 1e-5 --per_device_train_batch_size 8
$ python 1-to-ans_train.py --model_name_or_path shibing624/text2vec-base-chinese --output_dir 1-to-ans_e5b4l1_t2v --num_train_epochs 5 --learning_rate 1e-5 --per_device_train_batch_size 4
$ python 1-to-ans_train.py --model_name_or_path shibing624/text2vec-base-chinese --output_dir 1-to-ans_e5b8l1_t2v --num_train_epochs 5 --learning_rate 1e-5 --per_device_train_batch_size 8
```

這步完成之後會也會生成三個 model，因為執行時間有限，所以這三個 model 會透過 `download.sh` 下載。

程式碼主要是從 `run_qa_no_trainer.py` [3] 取 training 的部份再做修改，有做調整的 hyper parameter 如下：

| arguments                       | value                                                        |
| ------------------------------- | ------------------------------------------------------------ |
| `--max_seq_length`              | `512`                                                        |
| `--model_name_or_path`          | `hfl/chinese-roberta-wwm-ext` or `shibing624/text2vec-base-chinese` |
| `--per_device_train_batch_size` | `4` or `8`                                                   |
| `--per_device_eval_batch_size`  | `1`                                                          |
| `--learning_rate`               | `1e-5`                                                       |
| `--num_train_epochs`            | `5`                                                          |
| `--gradient_accumulation_steps` | `4`                                                          |

#### Step 2-3 Testing

```bash
$ python 1-to-ans_test.py --test_file final_test.json --model_name_or_path 1-to-ans_e5b4l1_t2v --output_csv output_e5b4l1_t2v.csv
$ python 1-to-ans_test.py --test_file final_test.json --model_name_or_path 1-to-ans_e5b8l1_t2v --output_csv output_e5b8l1_t2v.csv
$ python 1-to-ans_test.py --test_file final_test.json --model_name_or_path 1-to-ans_e5b8l1_hfl --output_csv output_e5b8l1_hfl.csv
```

這步完成之後會用剛剛生成的三個 model 預測結果，並產生三個相對應的 csv file。

程式碼主要是從 `run_qa_no_trainer.py` [3] 取 testing 的部份再做修改，有做調整的參數如下：

| arguments              | value                                                       |
| ---------------------- | ----------------------------------------------------------- |
| `--model_name_or_path` | 三個 model 不一樣（對應 `4-to-1_train.py` 的 `output_dir`） |

#### Step 2-4 Data Post-processing

```bash
$ python bracket_filled.py --test_file output_e5b4l1_t2v.csv --out_file output_e5b4l1_t2v_final.csv
$ python bracket_filled.py --test_file output_e5b8l1_t2v.csv --out_file output_e5b8l1_t2v_final.csv
$ python bracket_filled.py --test_file output_e5b8l1_hfl.csv --out_file output_e5b8l1_hfl_final.csv
```

這步主要是將可能不合理的答案改成較合理的答案，例如：如果預測結果只有左括弧卻沒有右括弧，則會在答案的最後補上右括弧。這樣做能夠稍微提升正確率。

#### Step 2-5 Voting

```bash
$ python 1-to-ans_voting.py --out_file ${3}
```

這步主要是在做投票，這裡會以 `hfl` 訓練出來的模型為主，也就是說如果三種模型預測的結果都不一樣，則會以 `hfl` 的結果當作答案。反之，如果有兩個以上的模型預測相同的答案，就會以該答案為最終結果。完成之後會在 `run.sh` 給定的路徑生成最終的結果。

相關資料：

[1] `run_swag_no_trainer.py`原始碼

https://github.com/huggingface/transformers/blob/main/examples/pytorch/multiple-choice/run_swag_no_trainer.py

[2] Multiple choice 相關資料

https://huggingface.co/docs/transformers/tasks/multiple_choice

[3] `run_qa_no_trainer.py`原始碼

https://github.com/huggingface/transformers/blob/main/examples/pytorch/question-answering/run_qa_no_trainer.py

[4] Question answering 相關資料

https://huggingface.co/docs/transformers/tasks/question_answering