#!/usr/bin/env python3

"""Parse Slack export and produce text files for linguistic analysis"""

import argparse
import glob
import json
import re
import csv
import os

parser = argparse.ArgumentParser()
parser.add_argument("dir_to_parse")
parser.add_argument("team_members_file")
args = parser.parse_args()


def get_team_members():
    team_members = []
    with open(args.team_members_file) as csv_file:
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
    return team_members


def get_text_result(member, team_members):
    files_to_parse = args.dir_to_parse + "/*.json"
    member_text = ""
    team_text = ""
    team_except_current_member = team_members.copy()
    team_except_current_member.remove(member)
    for f in sorted(glob.glob(files_to_parse)):
        with open(f, "r") as infile:
            messages = json.load(infile)
            for m in messages:
                if m['user'] == member:
                    member_text = member_text + " " + m['text']
                elif m['user'] in team_except_current_member:
                    team_text = team_text + " " + m['text']
    # Remove user mentions
    x = re.sub("<@[a-zA-Z0-9]*>", "", member_text)
    y = re.sub("<@[a-zA-Z0-9]*>", "", team_text)
    # Remove colons from emojis to retain text
    em = re.sub(r"\:([\S]*)\:", r"\1", x)
    et = re.sub(r"\:([\S]*)\:", r"\1", y)
    return em, et


def create_file(filepath, content):
    print(f'Output: {filepath}')
    with open(filepath, "w") as outfile:
        outfile.write(content)


def main():
    team_members = get_team_members()
    output_folder = args.dir_to_parse + "_lsm"
    if not os.path.exists(output_folder):
        print(f'Creating output folder {output_folder}')
        os.makedirs(output_folder)
    for member in team_members:
        member_text, team_text = get_text_result(member, team_members)
        create_file(output_folder + "/ONLY_" + member + ".txt", member_text)
        create_file(output_folder + "/EXCEPT_" + member + ".txt", team_text)
    print('Done!')


if __name__ == "__main__":
    main()
