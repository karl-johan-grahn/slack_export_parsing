# Parsing of Slack export

## Sample export
`KarlJohan_Slack_export_Feb_23_2021-Mar_24_2021` is an export from a private Slack instance.

## Team file
The scripts expects a comma separated team file with this file content, see [`team1.txt`](./team1.txt):
```
user,real_name
<slack user id>,Name of person 1
U.........,Name of person 2
```

## Slack export
Run the script [`slack_export.py`](./slack_export.py) to export messages from a Slack channel:
```
python slack_export.py <team_members_file> <channel_name> <channel_id>
```

## LSM Running the script
The [`lsm.py`](./lsm.py) script iterates over json files and exports the content from the members specified in a txt file:
```
python lsm.py <dir_to_parse> <team_members_file>
python lsm.py KarlJohan_Slack_export_Feb_23_2021-Mar_24_2021/general team1.txt
```

The above call produces an output folder `team1` with text content from members specified in `team1.txt`. The output can be processed with LIWC to get team cohesion metric.
