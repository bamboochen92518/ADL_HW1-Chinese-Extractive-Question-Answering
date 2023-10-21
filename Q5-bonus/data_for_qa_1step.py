import json

train_file = "train.json"
valid_file = "valid.json"
test_file = "test.json"
context_file = "context.json"

new_train_file = "train-1-step.json"
new_valid_file = "valid-1-step.json"
new_test_file = "test-1-step.json"

with open(train_file, 'r') as file:
    data = json.load(file)

with open(valid_file, 'r') as file:
    vdata = json.load(file)

with open(test_file, 'r') as file:
    tdata = json.load(file)

with open(context_file, 'r') as file:
    context = json.load(file)

# write output to json
for f in [[train_file, new_train_file], [valid_file, new_valid_file]]:
    with open(f[0], 'r') as file:
        data = json.load(file)
    data_list = list()
    for i in range(len(data)):
        tmp = ""
        start = data[i]["answer"]["start"]
        is_answer = 0
        for j in range(4):
            tmp += context[data[i]["paragraphs"][j]]
            if data[i]["paragraphs"][j] == data[i]["relevant"]:
                is_answer = 1
            elif is_answer == 0:
                start += len(context[data[i]["paragraphs"][j]])
        dictionary = {
            "id": data[i]["id"],
            "question": data[i]["question"],
            "context": tmp,
            "answers": {'answer_start': [start], 'text': [data[i]["answer"]["text"]]},
        }
        data_list.append(dictionary)

    with open(f[1], "w", encoding="utf8") as outfile:
        json.dump(data_list, outfile, ensure_ascii=False, indent=4)

with open(test_file, 'r') as file:
    data = json.load(file)
data_list = list()
for i in range(len(data)):
    tmp = ""
    start = 0
    for j in range(4):
        tmp += context[data[i]["paragraphs"][j]]
    dictionary = {
        "id": data[i]["id"],
        "question": data[i]["question"],
        "context": tmp,
        "answers": {'answer_start': [0], 'text': [""]},
    }
    data_list.append(dictionary)

with open(new_test_file, "w", encoding="utf8") as outfile:
    json.dump(data_list, outfile, ensure_ascii=False, indent=4)
