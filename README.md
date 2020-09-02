# GitLab deployer 🚀


## Installation

```
pip install gitlab-deployer
```

## Usage 

```
deployer <command> <arguments>
```
Commands:

```
  deploy       - start deploy daemon 
  download     - download single artifact 
```

Arguments:

```
deploy

Options:
  --url TEXT             GitLab url
  --private_token TEXT   GitLab private token
  --project_id INTEGER   Project id
  --slack_web_hook TEXT  Slack web hook api
  --slack_channel TEXT   Slack channel (#deploy)
  --slack_username TEXT  Slack channel
  --deploy_script TEXT   Execute after download and unpack artifact
                         (./deploy.sh)
  --last_job_file TEXT   Last job file (last.txt)
  --interval INTEGER     Pull interval (5)
  --error_sleep INTEGER  Sleep on error (25)
  --verbosity TEXT       Verbosity (log.level=DEBUG)
  --ref TEXT             Git Branch
  --web_url TEXT         HTTP GET web hook
  --result_script TEXT   Result shell script. Execute after deployment.
  --test_slack           Test Slack Send Info
  --help                 Show this message and exit.


download

Options:
  --url TEXT            GitLab url
  --private_token TEXT  GitLab private token
  --project_id INTEGER  Project id
  --verbosity TEXT      Verbosity (log.level=DEBUG)
  --ref TEXT            Git Branch
  --help                Show this message and exit.

```




## Example

Command line
```

deployer deploy --ref master \
	--slack_web_hook=https://hooks.slack.com/services/xxxxxx/yyyyyy/zzzzzzzzzzzzz \
	--slack_channel="#deploy"  --slack_username="deploy-user"  --url http://gitlab.com \
	--private_token=tttttttttttttt --project_id=00

```

system.d example

```
[Unit]
Description=Deployer Service

[Service]
ExecStart=deployer deploy --ref master \
	--slack_web_hook=https://hooks.slack.com/services/xxxxxx/yyyyyy/zzzzzzzzzzzzz \
	--slack_channel="#deploy"  --slack_username="deploy-user"  --url http://gitlab.com \
	--private_token=tttttttttttttt --project_id=00


Restart=always
WorkingDirectory=/myproject/
StandardOutput=syslog
StandardError=syslog

[Install]
WantedBy=default.target
```

deploy.sh 

```
#!/bin/bash

unzip ./artifacts.zip
mv ./simple-java-project/target/simple-java-project.jar ./
systemctl restart simplejavaproject

echo "OK"
```

## Develop

Using [poetry](https://python-poetry.org/)

```
cd ./gitlab-deployer/
poetry install
```

Run with poetry
```
poetry run deployer <command> <args>

poetry run deployer deploy --help
```


Enjoy!