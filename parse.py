#!/usr/bin/python

import sys
import glob
import json
import re
import csv

if len(sys.argv) != 3:
    print("Error: Incorrect number of argument")
    print("parse.py <dir_to_parse> <team_members>")
    sys.exit(2)

team_members = []
with open(sys.argv[2]) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names in team file are {", ".join(row)}')
            line_count += 1
        else:
            team_members.append(row[0])
            line_count += 1
    print(f'Processed {line_count-1} members')

text_result = ""
files_to_parse = sys.argv[1] + "/*.json"
# Go through the files in sorted order
print("Starting to process json files")
for f in sorted(glob.glob(files_to_parse)):
    with open(f, "r") as infile:
        messages = json.load(infile)
    for m in messages:
        if m['user'] in team_members:
            text_result = text_result + " " + m['text']

# Remove user mentions from combined text
x = re.sub("<@[a-zA-Z0-9]*>", "", text_result)

output = "output.txt"
print(f'Output: {output}')
with open(output, "w") as outfile:
    outfile.write(x)
