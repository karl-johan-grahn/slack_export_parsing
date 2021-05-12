#!/usr/bin/env python3
'''
Script to export Slack messages from a channel.
You have to create a Slack Bot and invite it to the channel.
Then provide the bot token to this script with the file specifying
team members whose content should be exported and
channel name and channel id.
'''

import argparse
import csv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import json
import time
import datetime
import os
import sys

TOKEN=os.getenv('SLACK_BOT_TOKEN')
if not(TOKEN):
    print("Error: Slack bot token environment variable is not set")
    sys.exit(2)

parser = argparse.ArgumentParser()
parser.add_argument("team_members_file")
parser.add_argument("channel_name")
parser.add_argument("channel_id")
args = parser.parse_args()

start1 = "1/3/2019"
end1   = "1/3/2020"
start2 = "1/3/2020"
end2   = "1/3/2021"

def timeStamp(s):
    return time.mktime(datetime.datetime.strptime(s, "%d/%m/%Y").timetuple())

start1_ts = timeStamp(start1)
end1_ts = timeStamp(end1)
start2_ts = timeStamp(start2)
end2_ts = timeStamp(end2)

client = WebClient(token=TOKEN)

def export_channel(channel_name, channel_id, team_members, oldest_ts, latest_ts, suffix):
    try:
        print(f'Getting messages from "{channel_name}" for members {team_members}')
        result = client.conversations_history(channel=channel_id, oldest=oldest_ts, latest=latest_ts)
        all_message = []
        for m in result["messages"]:
            if m['user'] in team_members:
                all_message.append(m)
        while result['has_more']:
            print("\tGetting more...")
            result = client.conversations_history(channel=channel_id, oldest=oldest_ts, latest=latest_ts, cursor=result['response_metadata']['next_cursor'])
            for m in result["messages"]:
                if m['user'] in team_members:
                    all_message.append(m)
        # Save to disk
        filename = f'{channel_name}_{suffix}.json'
        print(f'  Downloaded {len(all_message)} messages from {channel_name}.')
        print('  Saving to', filename)
        with open(filename, 'w') as outfile:
            json.dump(all_message, outfile)
    except SlackApiError as e:
        print("Error using conversation: {}".format(e))

def get_team_members():
    team_members = []
    with open(args.team_members_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                team_members.append(row[0])
                line_count += 1
        print(f'Read {line_count-1} members from team file')
    return team_members

if __name__ == "__main__":
    team_members = get_team_members()
    export_channel(args.channel_name, args.channel_id, team_members, start1_ts, end1_ts, "before")
    export_channel(args.channel_name, args.channel_id, team_members, start2_ts, end2_ts, "during")
