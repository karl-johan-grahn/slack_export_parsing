#!/usr/bin/python

import sys
import glob
import json

if len(sys.argv) != 2:
    print("Error: Missing directory to merge json files")
    sys.exit(2)

result = []
files_to_merge = sys.argv[1] + "/*.json"
print("Starting to merge all json files in:", files_to_merge)
for f in glob.glob(files_to_merge):
    with open(f, "r") as infile:
        result.append(json.load(infile))

merged_filename = "merged_file.json"
json_object = json.dumps(result, indent=4)
with open(merged_filename, "w") as outfile:
    outfile.write(json_object)

print("Successfully merged all files to:", merged_filename)
