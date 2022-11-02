#!/usr/bin/env bash
#
##########################################################
# Get Delegate docker-compose file and deploy it locally #
##########################################################
#
#
print_color(){
  GREEN=$(tput setaf 2)
  NC=$(tput sgr0)
  echo -e " "
  echo  -e "*${GREEN} ${1} ${NC} "
  
}
# check if  docker and kubectl are installed.

if ! [ -x "$(command -v kubectl)" ]; then
  print_color 'Error: kubectl is not installed.' >&2
  exit 1
fi

if ! [ -x "$(command -v docker)" ]; then
  print_color 'Error: docker is not installed.' >&2
  exit 1
fi

#install k3ds
print_color " Installing k3ds..  "
bash installk3d.sh
print_color "  Installing k3ds -- completed ..  "

#create single node cluster
print_color "Creating single node cluster..   "
k3d cluster create mylocalcluster
print_color "  Creating single node cluster -- completed  "

#create delegate token
print_color "  Creating delegate token and delegate.yml.  "
curl -X POST "https://app.harness.io/gateway/ng/api/delegate-token-ng?accountIdentifier=${ACCOUNTIDENTIFIER}&orgIdentifier=${ORGIDENTIFIER}&projectIdentifier=${PROJECTIDENTIFIER}&tokenName=${TOKENIDENTIFIER}" -H "x-api-key: ${APIKEY}" -H "Content-Length: 0" --silent --show-error

#download kubernetes delegate mainifest
curl -X POST "https://app.harness.io/gateway/ng/api/download-delegates/docker?accountIdentifier=${ACCOUNTIDENTIFIER}&orgIdentifier=${ORGIDENTIFIER}&projectIdentifier=${PROJECTIDENTIFIER}" -H "Content-Type: application/json" -H "x-api-key: ${APIKEY}" -o "docker-compose.yml" --silent --show-error --data-binary @- <<DATA
{
    "name": "${KUBAENETESDELEGATENAME}",
    "size": "LAPTOP",
    "tags": [
      "string"
    ],
    "tokenName": "${TOKENIDENTIFIER}",
    "clusterPermissionType": "CLUSTER_ADMIN"
  }
DATA
print_color "--"
print_color "creating delegate token and delegate.yml -- completed  "

# apply delegate in cluster
print_color "  apply delegate Docker compose  "
docker-compose -f docker-compose.yml up -d
print_color " delegate applied successfully -- completed"

print_color "Creating Service Account with cluster admin role in k3d cluster"
kubectl create serviceaccount myserviceaccount
kubectl create clusterrolebinding comman-admin-sa-crb --clusterrole=cluster-admin --serviceaccount=default:myserviceaccount
print_color "Use Below Service Account Token while setting up kubernets connector "
kubectl create token  myserviceaccount 
print_color "Use below  url as master node url for kuberntes connector setup"
export KPORT=$(kubectl cluster-info  | head -n 1 | sed 's/.*://')
export KIP=$(ifconfig | grep -E "([0-9]{1,3}\.){3}[0-9]{1,3}" | grep -v 127.0.0.1 | head -1 | awk '{ print $2 }')
echo "https://${KIP}:${KPORT}"
