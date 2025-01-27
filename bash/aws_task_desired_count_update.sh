#!/usr/bin/env bash

set -e

# Restarts services in tasks
cluster_name=dev-employee-tce-transformer-employee-tce-transformer-kafkaWorkerFargateCluster932BF615-rK62vlHtngrA
desired_count=1

service_list=$(aws ecs list-services --region eu-central-1 --profile dev --cluster "$cluster_name" | jq -rC '.serviceArns.[]')

for servicename in $service_list; do
    echo Setting desired count $desired_count to "$servicename"
    aws ecs update-service --region eu-central-1 --profile dev --cluster "$cluster_name" --service "$servicename" --desired-count $desired_count | jq -rC '.service | del(.deployments) | del(.events)'
done
