import json

train_file = "train.json"
valid_file = "valid.json"
context_file = "context.json"

new_train_file = "train_for_qa.json"
new_valid_file = "valid_for_qa.json"

with open(train_file, 'r') as file:
    data = json.load(file)

with open(valid_file, 'r') as file:
    vdata = json.load(file)

with open(context_file, 'r') as file:
    context = json.load(file)

# write output to json
data_list = list()
for i in range(len(data)):
    dictionary = {
        "id": data[i]["id"],
        "question": data[i]["question"],
        "context": context[data[i]["relevant"]],
        "answers": {'answer_start': [data[i]["answer"]["start"]], 'text': [data[i]["answer"]["text"]]},
    }
    data_list.append(dictionary)

print(type(data[i]["answer"]["start"]))

with open(new_train_file, "w", encoding="utf8") as outfile:
    json.dump(data_list, outfile, ensure_ascii=False, indent=4)

vdata_list = list()
for i in range(len(vdata)):
    dictionary = {
        "id": vdata[i]["id"],
        "question": vdata[i]["question"],
        "context": context[vdata[i]["relevant"]],
        "answers": {'answer_start': [vdata[i]["answer"]["start"]], 'text': [vdata[i]["answer"]["text"]]},
    }
    vdata_list.append(dictionary)

with open(new_valid_file, "w", encoding="utf8") as outfile:
    json.dump(vdata_list, outfile, ensure_ascii=False, indent=4)
