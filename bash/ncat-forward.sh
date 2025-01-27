#!/usr/bin/env bash

# Forward some aws-dev port to localhost port using ncat.

pod_name="kaustuv-ncat"
remote_server="internal-dev-ebdr-supervisor-alb-448256886.eu-central-1.elb.amazonaws.com"
remote_port=80
local_port=8282

kubectl delete pods/"${pod_name}"

# "ncat --sh-exec \"ncat dev-audit-log-api-ro.rhwmzf.ng.0001.euc1.cache.amazonaws.com 6379\" -l 12456 --keep-open"
overrides='
{
  "spec": {
    "containers": [
      {
        "name": "'$pod_name'",
        "image": "raesene/ncat",
        "command": [
                  "sh",
                  "-c",
                  "ncat --sh-exec \"ncat '${remote_server}' '${remote_port}'\" -l '${local_port}' --keep-open"
                ],
        "resources": {
          "requests": {
            "cpu": "100m",
            "memory": "256Mi"
          },
          "limits": {
            "cpu": "100m",
            "memory": "256Mi"
          }
        }
      }
    ]
  }
}
'

kubectl run \
    "${pod_name}" \
    --image 'raesene/ncat' \
    --labels "service=${pod_name}_service" \
    --namespace "dev" \
    --overrides "${overrides}" \
    --restart Never \

# Implement wait first
# kubectl port-forward pods/"${pod_name}" ${local_port}:${local_port}

