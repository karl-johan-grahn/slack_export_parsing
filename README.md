# Team Cohesion and Team Performance

This repository contains tools that were used to extract and transform data needed for the dissertation _Local and remote team cohesion effect on performance in the software industry_ by [`Grahn` and `Martins` (2021)](https://www.diva-portal.org/smash/record.jsf?pid=diva2%3A1572012&dswid=-7928).

The Slack exports are used to calculate LSM (Language Style Matching) scores to estimate the team cohesion.

There is also a script for getting GitLab merge requests as part of estimating team performance.

## Team Cohesion

Team cohesion is measured through LSM score based on Slack content.

### Sample Manual Slack Export

[`KarlJohan_Slack_export_Feb_23_2021-Mar_24_2021`](./KarlJohan_Slack_export_Feb_23_2021-Mar_24_2021/) contains the result from a manual export of messages from two channels [`general`](./KarlJohan_Slack_export_Feb_23_2021-Mar_24_2021/general) and [`test`](./KarlJohan_Slack_export_Feb_23_2021-Mar_24_2021/test) from a private Slack instance, and is made available only for test purposes. Similar exports can easily be done from any Slack instance.

A manual export cannot necessarily be restricted to certain channels, so for that reason a script is needed.

### Team File

The Slack export script takes a comma separated team file as input, containing the users whose messages should be included in the export. The file should have this structure:

```txt
user,real_name
<slack user id>,Name of person 1
U.........,Name of person 2
```

See [`before_team1.txt`](./before_team1.txt) for an example team file.

### Slack Export

To export content from a Slack channel:

1. Create a Slack Bot
1. Create a token for the bot
1. Invite the bot to the channel that you want to export content from
1. Set the bot token as an environment variable `SLACK_BOT_TOKEN`
1. Run the script [`slack_export.py`](./slack_export.py) to export messages from the Slack channel:

    ```sh
    python slack_export.py [team_file] [channel_name] [channel_id]
    ```

The output will be a folder for each team containing a JSON file with all the messages and threads from the specified channel from the specified team members for two time periods.

### Merge JSON Files

If multiple JSON output files are created, you need to merge them to a single file using the script [`merge.py`](./merge.py):

```sh
python merge.py [dir_to_parse]
```

For example:

```sh
python merge.py KarlJohan_Slack_export_Feb_23_2021-Mar_24_2021/general
```

### Remove User Mentions

To remove Slack user mentions from JSON output, run the script [`parse.py`](./parse.py):

```sh
python parse.py [dir_to_parse] [team_members_file]
```

### LSM (Language Style Matching) Score

To extract the content to calculate the LSM score for each team:

1. Run the [`lsm.py`](./lsm.py) script:

    ```sh
    python lsm.py [dir_to_parse] [team_members_file]
    ```

    For example:

    ```sh
    python lsm.py KarlJohan_Slack_export_Feb_23_2021-Mar_24_2021/general before_team1.txt
    ```

1. The script iterates over the JSON files in the input folder `KarlJohan_Slack_export_Feb_23_2021-Mar_24_2021/general` and exports the messages from the members specified in the input team file `before_team1.txt` to a folder with the same name as the input folder with `_lsm` appended: `general_lsm`. It removes user mentions to anonymize the text, and removes colons from emojis to retain the emoji text and their meaning.
1. The output in this folder can be processed with a dictionary such as [LIWC](https://www.liwc.app/) to get:
    * The total word count
    * The percentage of total words in the text that match each of the dictionary categories that are relevant for calculating the LSM score

The [`KarlJohan_Slack_export_Feb_23_2021-Mar_24_2021/general_lsm`](./KarlJohan_Slack_export_Feb_23_2021-Mar_24_2021/general_lsm) folder is an example output with a spreadsheet that can be used as a template to calculate the LSM score.

## Team Performance

Team performance is based on team efficiency comparisons using DEA (Data Envelopment Analysis).

## Git Contributions

To get git contributions during two time periods, use the [`gitlab.sh`](./gitlab.sh) script:

```sh
gitlab.sh [metadata_file]
```

## Team Efficiency via DEA

The [`team_efficiency`](https://github.com/karl-johan-grahn/team_efficiency) repository contains `R` code for doing DEA calculations.
