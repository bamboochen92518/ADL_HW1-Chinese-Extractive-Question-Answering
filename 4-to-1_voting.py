import json

testA = "4-to-1_bert.json"
testB = "4-to-1_hfl.json"
testC = "4-to-1_t2v.json"
testF = "final_test.json"

with open(testA, 'r') as file:
    dataA = json.load(file)

with open(testB, 'r') as file:
    dataB = json.load(file)

with open(testC, 'r') as file:
    dataC = json.load(file)

# write output to json
data_list = list()
for i in range(len(dataA)):
    context = dataA[i]["context"]
    if dataB[i]["context"] == dataC[i]["context"]:
        context = dataB[i]["context"]
    dictionary = {
        "id": dataA[i]["id"],
        "question": dataA[i]["question"],
        "context": context,
        "answers": dataA[i]["answers"],
    }
    data_list.append(dictionary)

with open(testF, "w", encoding="utf8") as outfile:
    json.dump(data_list, outfile, ensure_ascii=False, indent=4)
