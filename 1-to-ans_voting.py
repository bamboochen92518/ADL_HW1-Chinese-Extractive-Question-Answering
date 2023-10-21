import argparse
import csv
parser = argparse.ArgumentParser()
parser.add_argument("--out_file", type=str, default="output_final.csv")
args = parser.parse_args()

testA = "output_e5b8l1_hfl_final.csv"
testB = "output_e5b8l1_t2v_final.csv"
testC = "output_e5b4l1_t2v_final.csv"
testF = args.out_file

dataA = list()
dataB = list()
dataC = list()

with open(testA, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        dataA.append(row)

with open(testB, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        dataB.append(row)

with open(testC, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        dataC.append(row)

length = len(dataA)
data_list = list()

for i in range(length):
    if dataB[i][1] == dataC[i][1]:
        dataA[i][1] = dataB[i][1]
    data_list.append(dataA[i])

with open(testF, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(data_list)
