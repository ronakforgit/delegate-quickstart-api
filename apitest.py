# create  a bash script which  installs all dependencies
# then installs a k3d cluster

import requests
import yaml
import os
def populate_yaml(value_dict):
    with open('file_to_edit.yaml') as f:
        doc = yaml.load(f)

    # doc['state'] = state

    with open('file_to_edit.yaml', 'w') as f:
        yaml.dump(doc, f)
    return (value_dict)

def create_project(apikey,accountIdentifier,projectidentifier='TestProject'): 

    headers = {
        # Already added when you pass json= but not when you pass data=
        # 'Content-Type': 'application/json',
        'x-api-key': apikey,
    }

    params = {
        'accountIdentifier': accountIdentifier,
        'orgIdentifier': 'default',
    }

    json_data = {
        'project': {
            'orgIdentifier': 'default',
            'identifier': projectidentifier,
            'name': 'testproject',
            'color': 'green',
            'modules': [
                'CD',
            ],
            'description': 'string',
            'tags': {
                'property1': 'string',
                'property2': 'string',
            },
        },
    }

    response = requests.post('https://app.harness.io/gateway/ng/api/projects', params=params, headers=headers, json=json_data)
    return (response)
   
def create_delegate(apikey,accountIdentifier,projectidentifier,token):
    headers = {
        'x-api-key': apikey,
    }

    params = {
        'accountIdentifier': accountIdentifier,
        'orgIdentifier': 'default',
        'projectIdentifier': projectidentifier,
        'tokenName': token,
    }

    response = requests.post('https://app.harness.io/gateway/ng/api/delegate-token-ng', params=params, headers=headers)    
    return (response)

def download_delegate_mainfist(apikey,accountIdentifier,projectidentifier,token,delegatename) :
    headers = {
        # Already added when you pass json= but not when you pass data=
        # 'Content-Type': 'application/json',
        'x-api-key': apikey,
    }

    params = {
        'accountIdentifier': accountIdentifier,
        'orgIdentifier': 'default',
        'projectIdentifier': projectidentifier,
    }

    json_data = {
        'name': delegatename,
        'description': 'test docker delegate description',
        'size': 'LAPTOP',
        'tags': [
            'string',
        ],
        'tokenName': token,
        'clusterPermissionType': 'CLUSTER_ADMIN',
        'customClusterNamespace': 'default',
    }

    response = requests.post('https://app.harness.io/gateway/ng/api/download-delegates/kubernetes', params=params, headers=headers, json=json_data)
    return(response)

def create_secret(apikey,accountIdentifier,projectidentifier,secretname,value) :

    headers = {
        # Already added when you pass json= but not when you pass data=
        # 'Content-Type': 'application/json',
        'x-api-key': apikey,
    }

    params = {
        'accountIdentifier': accountIdentifier,
        'privateSecret': 'false',
        'orgIdentifier': 'default',
        'projectIdentifier': projectidentifier
    }

    json_data = {
        'secret': {
            'type': 'SecretText',
            'name': secretname,
            'orgIdentifier': 'default',
            'projectIdentifier': projectidentifier,
            'identifier': secretname.lower(),
            'spec': {
                'errorMessageForInvalidYaml': 'string',
                'type': 'SecretTextSpec',
                'secretManagerIdentifier': 'harnessSecretManager',
                'valueType': 'Inline',
                'value': value

            },
        },
    }

    response = requests.post('https://app.harness.io/gateway/ng/api/v2/secrets', params=params, headers=headers, json=json_data)
    return(response)
   
def create_github_connector(apikey,accountIdentifier,projectidentifier,githuburl,githubusername,gitsecret,delegatename,pipelinereponame,githubconnectorid):

    headers = {
        # Already added when you pass json= but not when you pass data=
        # 'Content-Type': 'application/json',
        'x-api-key': apikey,
    }

    params = {
        'accountIdentifier': accountIdentifier,
        'isNewBranch': 'false',
        'baseBranch': 'string',
        'storeType': 'INLINE',
    }

    json_data = {
        'connector': {
            'name': 'Github Connector',
            'identifier': githubconnectorid,
            'orgIdentifier': 'default',
            'projectIdentifier': projectidentifier,
            'type': 'Github',
            'spec': {
                'connectorType': 'Github',
                'url': githuburl,
                'validationRepo': pipelinereponame,
                'authentication': {
                    "type": "Http",
                    "spec": {
                        "type": "UsernameToken",
                        "spec": {
                        "username": githubusername,
                        "usernameRef": None,
                        "tokenRef": gitsecret,
                        }
                    }
                },
                "delegateSelectors": [],
                "executeOnDelegate": False,
                "type": "Account"

            },
        },
    }

    response = requests.post('https://app.harness.io/gateway/ng/api/connectors', params=params, headers=headers, json=json_data)
    return(response)

def create_docker_connector(apikey,accountIdentifier,projectidentifier,dockerconectorid,dockerregistryurl,dockerusername,dockersecret) :
    headers = {
        # Already added when you pass json= but not when you pass data=
        # 'Content-Type': 'application/json',
        'x-api-key': apikey,
    }

    params = {
        'accountIdentifier': accountIdentifier,
        'isNewBranch': 'false',
        'baseBranch': 'string',
        'storeType': 'INLINE',
    }

    json_data = {
        'connector': {
        "name": 'Docker Connector',
        "identifier": dockerconectorid,
        "orgIdentifier": "default",
        "projectIdentifier": projectidentifier,
        "type": "DockerRegistry",
        "spec": {
            "dockerRegistryUrl": dockerregistryurl,
            "providerType": "DockerHub",
            "auth": {
                "type": "UsernamePassword",
                "spec": {
                    "username": dockerusername,
                    "usernameRef": None,
                    "passwordRef": dockersecret
                }
            },
            "delegateSelectors": [],
            "executeOnDelegate": False
        }
    },
    }

    response = requests.post('https://app.harness.io/gateway/ng/api/connectors', params=params, headers=headers, json=json_data)
    return(response)

def create_service(apikey,accountIdentifier,projectidentifier,servicename):
    
    with open('service.yaml', 'r') as file:
        yamlstring = file.read()
    headers = {
        # Already added when you pass json= but not when you pass data=
        # 'Content-Type': 'application/json',
        'x-api-key': apikey,
    }

    params = {
        'accountIdentifier': accountIdentifier,
    }

    json_data = {
        'identifier': servicename,
        'orgIdentifier': 'default',
        'projectIdentifier': projectidentifier,
        'name': servicename,
        'description': 'string',
        "yaml": yamlstring
    }

    response = requests.post('https://app.harness.io/gateway/ng/api/servicesV2', params=params, headers=headers, json=json_data)
    return(response)

def create_env(apikey,accountIdentifier,projectidentifier,envname):
    headers = {
        # Already added when you pass json= but not when you pass data=
        # 'Content-Type': 'application/json',
        'x-api-key': apikey,
    }

    params = {
        'accountIdentifier': accountIdentifier,
    }

    json_data = {
        'orgIdentifier': 'default',
        'projectIdentifier': projectidentifier,
        'identifier': envname,
        'name': envname,
        'type': 'PreProduction',

    }
    response = requests.post('https://app.harness.io/gateway/ng/api/environmentsV2', params=params, headers=headers, json=json_data)
    return(response)

def create_pipeline(apikey,accountIdentifier,projectidentifier):
    headers = {
        'Content-Type': 'application/yaml',
        'x-api-key': apikey,
    }

    params = {
        'accountIdentifier': accountIdentifier,
        'orgIdentifier': 'default',
        'projectIdentifier': projectidentifier,
    }

    # data = 'pipeline:\n      name: Sample Pipeline\n      identifier: Sample_Pipeline\n      allowStageExecutions: false\n      projectIdentifier: Temp\n      orgIdentifier: default\n      tags: {}\n      stages:\n          - stage:\n                name: Sample Stage\n                identifier: Sample_Stage\n                description: ""\n                type: Approval\n                spec:\n                    execution:\n                        steps:\n                            - step:\n                                  name: Approval Step\n                                  identifier: Approval_Step\n                                  type: HarnessApproval\n                                  timeout: 1d\n                                  spec:\n                                      approvalMessage: |-\n                                          Please review the following information\n                                          and approve the pipeline progression\n                                      includePipelineExecutionHistory: true\n                                      approvers:\n                                          minimumCount: 1\n                                          disallowPipelineExecutor: false\n                                          userGroups: <+input>\n                                      approverInputs: []\n                            - step:\n                                  type: ShellScript\n                                  name: ShellScript Step\n                                  identifier: ShellScript_Step\n                                  spec:\n                                      shell: Bash\n                                      onDelegate: true\n                                      source:\n                                          type: Inline\n                                          spec:\n                                              script: <+input>\n                                      environmentVariables: []\n                                      outputVariables: []\n                                      executionTarget: {}\n                                  timeout: 10m\n                tags: {}\n          - stage:\n                name: Sample Deploy Stage\n                identifier: Sample_Deploy_Stage\n                description: ""\n                type: Deployment\n                spec:\n                    serviceConfig:\n                        serviceRef: <+input>\n                        serviceDefinition:\n                            spec:\n                                variables: []\n                            type: Kubernetes\n                    infrastructure:\n                        environmentRef: <+input>\n                        infrastructureDefinition:\n                            type: KubernetesDirect\n                            spec:\n                                connectorRef: <+input>\n                                namespace: <+input>\n                                releaseName: release-<+INFRA_KEY>\n                        allowSimultaneousDeployments: false\n                    execution:\n                        steps:\n                            - step:\n                                  name: Rollout Deployment\n                                  identifier: rolloutDeployment\n                                  type: K8sRollingDeploy\n                                  timeout: 10m\n                                  spec:\n                                      skipDryRun: false\n                        rollbackSteps:\n                            - step:\n                                  name: Rollback Rollout Deployment\n                                  identifier: rollbackRolloutDeployment\n                                  type: K8sRollingRollback\n                                  timeout: 10m\n                                  spec: {}\n                tags: {}\n                failureStrategies:\n                    - onFailure:\n                          errors:\n                              - AllErrors\n                          action:\n                              type: StageRollback\n  '
    with open('testk8s.yaml', 'r') as file:
        data = file.read()

    response = requests.post('https://app.harness.io/gateway/pipeline/api/pipelines/v2', params=params, headers=headers, data=data)
    return (response)

apikey=os.environ['APIKEY']
accountIdentifier=os.environ['ACCOUNTIDENTIFIER']
dockerPat=os.environ['DOCKERPAT']
githubPat=os.environ['GITPAT']
projectidentifier='TestProject'
tokenName='merabharatmahan4'
delegatename='test-delegateclear'
gitsecret='gitsecret'
dockersecret='dockersecret'
gitHubAccountURL='https://github.com/ronakforgit'
githubUserName='ronakforgit'
githubPipelineRepo='test'
githubconnectorid='githubconnector'
dockerconectorid='dockerconector'
dockerregistryurl='https://registry.hub.docker.com/v2/'
dockerusername='ronakpatildocker'
servicename='k8service'
envname='dev'


#     #create project , create token , download docker delegate yaml
print ("creating project")
response=create_project(apikey,accountIdentifier,projectidentifier)
print (response)

print ("creating token")
tokenValue = create_delegate(apikey,accountIdentifier,projectidentifier,tokenName).json()['resource']["value"]
print(tokenValue)

print ("downloading docker delegate yaml")
response =download_delegate_mainfist(apikey,accountIdentifier,projectidentifier,tokenName,delegatename)
data= (response.content)
with open("k8delegate.yml", 'wb') as s:
    s.write(data)

#apply delegate and wait till its connected - while !connected hit api 

print("creating gitsecret")
# create githubPaat secret
response = create_secret(apikey,accountIdentifier,projectidentifier,gitsecret,githubPat)
print(response)

print("creating dockersecret")
#create DockerPat secret
response = create_secret(apikey,accountIdentifier,projectidentifier,dockersecret,dockerPat)
print(response)

print("creating git conector")
# create github and docker conector
response = create_github_connector(apikey,accountIdentifier,projectidentifier,gitHubAccountURL,githubUserName,gitsecret,delegatename,pipelinereponame=githubPipelineRepo,githubconnectorid=githubconnectorid)
print(response)

print("creating dockerconector")
# create dockerconector
response= create_docker_connector(apikey,accountIdentifier,projectidentifier,dockerconectorid,dockerregistryurl,dockerusername,dockersecret)
print(response)

print("creating servive")
response= create_service(apikey,accountIdentifier,projectidentifier,servicename)
print(response)

print("creating env")
response= create_env(apikey,accountIdentifier,projectidentifier,envname)
print(response)

print("creating pipeline")
response= create_pipeline(apikey=apikey,accountIdentifier=accountIdentifier,projectidentifier=projectidentifier)
print(response)

# Sign Up
# Create Project
# Choose CD Module
# Download and Deploy Delegate (Delegate First Approach) [Docker Based Delegate]
# Create Secrets
# - Git Pat
# - Docker Pat
# Connectors
# - Docker Connector
# - Git Connector
# Pipeline
# - New Pipeline > Import from Git
# Add Manifest 
# Add Artifact
# Add Environment -> rancher/k3s docker image
# Finally!! Execute Pipeline - yay