# Not Pre-trained Model

### Step 1. Training

```bash
$ python 4-to-1_no_pretrain.py
```

程式碼主要是從 `../4-to-1_train.py`做修改，程式碼異動如下：

1. Config

   原始：

   ```python
   config = AutoConfig.from_pretrained(args.model_name_or_path, trust_remote_code=args.trust_remote_code)
   ```

   更改後：

   ```python
   config = BertConfig()
   ```

2. Model

   原始：

   ```python
   model = AutoModelForMultipleChoice.from_pretrained(
               args.model_name_or_path,
               from_tf=bool(".ckpt" in args.model_name_or_path),
               config=config,
               trust_remote_code=args.trust_remote_code,
           )
   ```

   更改後：

   ```python
   model = AutoModelForMultipleChoice.from_config(config, trust_remote_code=args.trust_remote_code)
   ```

除了這兩個地方以外，都沒有做更動，包括hyper-parameter。以下列出 training 使用的 hyoer parameter 。

| arguments                       | value               |
| ------------------------------- | ------------------- |
| `--max_seq_length`              | `512`               |
| `--model_name_or_path`          | `bert-base-chinese` |
| `--per_device_train_batch_size` | `1`                 |
| `--per_device_eval_batch_size`  | `1`                 |
| `--learning_rate`               | `3e-5`              |
| `--num_train_epochs`            | `1`                 |
| `--gradient_accumulation_steps` | `2`                 |

以下為 performance 的比較：

|                 | eval accuracy       |
| --------------- | ------------------- |
| Pre-trained     | 0.9511465603190429  |
| Not Pre-trained | 0.47291458956463944 |