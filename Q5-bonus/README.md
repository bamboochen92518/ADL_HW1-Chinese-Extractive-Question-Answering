# Q5 End-to-end Transformer-based Model 

### Step 1 Data Pre-processing

```bash
$ python data_for_qa_1step.py
```

這步完成之後會將輸入轉換成 Question Answering 接受的格式。和前面的 Question Answering 不同的地方如下：

1. context 的部份為四個候選段落接起來
2. 如果 relevant 的段落不是第一段，answer start 的 index 要再加上前面段落的字數才會是正確的。

### Step 2 Training

```bash
$ python 1-step-train.py
```

這步完成之後會產生 model。

程式碼主要是從 `../1-to-ans_train.py`做修改。

### Step 3 Testing

```bash
$ python 1-step-test.py
```

這步會用剛剛訓練完的模型進行預測，完成之後會將預測結果輸出至指定的檔案。

程式碼主要是從 `../1-to-ans_test.py`做修改。