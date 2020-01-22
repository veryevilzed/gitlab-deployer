#!/usr/bin/env python

import os, logging, click, sys

from .deployer import Deployer
from .download import Download

FORMAT = '%(asctime)-7s [%(name)-6s] [%(levelname)-5s] %(message)s'
#logging.basicConfig(format=FORMAT, level=logging.INFO, datefmt="%H:%M:%S")
log = logging.getLogger("DEPLOYER")


@click.group()
def cli():
    pass

@cli.command()
@click.option('--url', default="http://gitlab.com/", help='GitLab url')
@click.option('--private_token', default="", help='GitLab private token')
@click.option('--project_id',  default=-1, help='Project id')
@click.option('--slack_web_hook', default="", help='Skack web hook api')
@click.option('--slack_channel', default="#deploy", help='Slack channel (#deploy)')
@click.option('--slack_username', default='Deployer', help='Slack channel')
@click.option('--deploy_script', default='./deploy.sh', help='Execute after download and unpack artifact (./deploy.sh)')
@click.option('--last_job_file', default='./last.txt', help='Last job file (last.txt)')
@click.option('--interval', default=5, help='Pull interval (5)')
@click.option('--error_sleep', default=25, help='Sleep on error (25)')
@click.option('--verbosity', default=False, help='Verbosity (log.level=DEBUG)')
@click.option('--ref', default="master", help='Git Branch')
def deploy(url, private_token, project_id, slack_web_hook, slack_channel, slack_username, deploy_script, last_job_file,
           interval, error_sleep, verbosity, ref):
    if private_token == "" and os.environ.get('GITLAB_PRIVATE_TOKEN'):
        private_token = os.environ.get('GITLAB_PRIVATE_TOKEN')

    if private_token=="":
        log.error("setup private token")
        sys.exit(1)

    if project_id == -1:
        log.error("setup project id")
        sys.exit(1)

    if verbosity:
        logging.basicConfig(format=FORMAT, level=logging.DEBUG, datefmt="%H:%M:%S")
    else:
        logging.basicConfig(format=FORMAT, level=logging.INFO, datefmt="%H:%M:%S")

    Deployer(url, private_token, project_id, slack_web_hook, slack_channel, slack_username, deploy_script, last_job_file,
           interval, error_sleep, ref)


@cli.command()
@click.option('--url', default="http://gitlab.com/", help='GitLab url')
@click.option('--private_token', default="", help='GitLab private token')
@click.option('--project_id',  default=-1, help='Project id')
@click.option('--verbosity', default=False, help='Verbosity (log.level=DEBUG)')
@click.option('--ref', default="master", help='Git Branch')
def download(url, private_token, project_id, verbosity, ref):
    if verbosity:
        logging.basicConfig(format=FORMAT, level=logging.DEBUG, datefmt="%H:%M:%S")
    else:
        logging.basicConfig(format=FORMAT, level=logging.INFO, datefmt="%H:%M:%S")

    Download(url, private_token, project_id, ref)


if __name__ == '__main__':
    cli()
