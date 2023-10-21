import argparse
import csv
parser = argparse.ArgumentParser()
parser.add_argument("--test_file", type=str, default="output.csv")
parser.add_argument("--out_file", type=str, default="oooutput.csv")
args = parser.parse_args()

row_list = list()

with open(args.test_file, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        if row[1].count("「") > row[1].count("」"):
            row[1] = row[1] + "」"
        if row[1].count("「") < row[1].count("」"):
            row[1] = "「" + row[1]
        if row[1].count("《") > row[1].count("》"):
            row[1] = row[1] + "》"
        if row[1].count("《") < row[1].count("》"):
            row[1] = "《" + row[1]
        row_list.append(row)

with open(args.out_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(row_list)
