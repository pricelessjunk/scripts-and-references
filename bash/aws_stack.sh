#!/bin/zsh

# Checks which connector stacks exists that are not part of the connectors repo.

aws_env='dev'
conn_repo=$HOME'/dev/ebdr-msk-connectors'

# allstacks=$(aws cloudformation list-stacks --profile $aws_env --region 'eu-central-1' --output json --query 'StackSummaries[*].StackName' | jq -r '.[] | .StackStatus=="UPDATE_COMPLETE"))
allstacks=$(aws cloudformation list-stacks --profile $aws_env --region 'eu-central-1' --output json | jq -r '.StackSummaries.[] | select(.StackStatus=="UPDATE_COMPLETE")' | jq -r ".StackName")

connector_names=$(echo $allstacks | grep -E '^[dev|prod].*ebdr-msk-connectors.*$' | while read l;do echo ${l#$aws_env'-ebdr-msk-connectors-'}; done;)
connector_names=$(echo $connector_names | sort) 
# echo $connector_names

connector_local=$(ls -1 $conn_repo/environments/$aws_env | sed -e 's/\.yaml$//')
connector_local=$(echo $connector_local | sort) 
# echo $connector_local

# echo $connector_names > remote
# echo $connector_local > local

echo '------ Diff  space   Corresponding lines are identical.'
echo '      "|"     Corresponding lines are different.'
echo '      "<"     Files differ and only the first file contains the line.'
echo '      ">"     Files differ and only the second file contains the line.'
echo '---- Remote Stacks -------------------------  Local Connector List -----'
diff -y <(echo $connector_names) <(echo $connector_local)
