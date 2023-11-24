#!/bin/bash
# Simple deploy script that wraps `kubectl` call.
#
# NAMESPACE: namespace that will be deployed. Valid values: staging and production

namespace=${1:-$NAMESPACE}

deployment_file=.deploy/deployment.yaml

echo $namespace

if [[ "$namespace" ]]; then
    microk8s kubectl -n $namespace apply -f $deployment_file

    # Rollout status
    microk8s kubectl -n $namespace rollout status deployments  neuromorphic-gs || {
        microk8s kubectl -n $namespace rollout undo deployments neuromorphic-gs; exit 1;
    }
else
  echo "Missing values! You must define: NAMESPACE!"
  exit 1
fi
