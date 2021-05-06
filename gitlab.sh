#!/bin/bash

if [ -z "$1" ]; then
    echo "Error: No git metadata file supplied"
    exit 1
fi

if [[ -z "${GITLAB_TOKEN}" ]]; then
    IFS= read -rs -p "Please enter your GitLab access token with api scope to query the server: " token
    echo
    if [[ -z "$token" ]]; then
        printf '%s\n' "Error: No token entered"
        exit 1
    fi
else
    token="${GITLAB_TOKEN}"
fi

gitlab_instance=""
users=()
counter=0

while read line; do
    if [ $counter -eq 0 ]; then
        gitlab_instance="$line"
    else
        users+=("$line")
    fi
    ((counter=counter+1))
done <$1

echo "GitLab contributions before Covid"
for u in ${users[@]}; do
    gitlab_url="$gitlab_instance/api/v4/users/$u/events?before=2020-03-01&after=2019-03-01&target_type=merge_request"
    response=$(curl -I --header "PRIVATE-TOKEN: $token" "$gitlab_url" 2>&1)
    xtotal=$(echo "$response" | grep x-total:)
    echo "$u: $xtotal"
done

echo "GitLab contributions during Covid"
for u in ${users[@]}; do
    gitlab_url="$gitlab_instance/api/v4/users/$u/events?before=2021-03-01&after=2020-03-01&target_type=merge_request"
    response=$(curl -I --header "PRIVATE-TOKEN: $token" "$gitlab_url" 2>&1)
    xtotal=$(echo "$response" | grep x-total:)
    echo "$u: $xtotal"
done
