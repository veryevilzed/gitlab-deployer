#coding:utf-8
import traceback

import gitlab, time, logging, zipfile, subprocess, requests, os
from os import path

log = logging.getLogger("DEPLOYER")


class Deployer:
    def __init__(self, url, private_token, project_id, slack, web, deploy_script, last_job_file,
           interval, error_sleep, ref, result_script, test_slack):
        self.gl = gitlab.Gitlab(url, private_token, api_version=4)
        self.result_script = result_script
        self.web = web

        self.slack_web_hook = slack["web_hook"]
        if "https://" in self.slack_web_hook:
            self.slack_url = slack["web_hook"]
        else:
            self.slack_url = "https://hooks.slack.com/services/" + slack["web_hook"]
        self.pending_job = -1
        self.failed_job = -1
        self.ref = ref
        slack_channel = slack["channel"]
        if slack_channel[0] != "#":
            slack_channel = "#"+slack_channel
        self.slack = {
            'channel': slack_channel,
            'icon': ":rocket:",
            'test': "",
            'username': slack["username"]
        }

        if test_slack:
            log.info("Send slack test message")
            self.send("Deployer is UP")

        self.project = self.gl.projects.get(project_id)
        self.deploy_script = deploy_script
        self.last_job_file = path.abspath(last_job_file)
        self.last_job = self.get_last_job_id()


        while(True):
            try:
                self.loop()
                time.sleep(interval)
            except Exception as e:
                log.error("Error:%s", e)
                self.send(":x: (%s)\n'%s'" % (e, traceback.format_exc().splitlines()))
                time.sleep(error_sleep)

    def save_last_job_id(self, id):
        f = open(self.last_job_file, 'w')
        f.write(str(id))
        f.close()
        self.last_job = id

    def get_last_job_id(self):
        if not os.path.isfile(self.last_job_file):
            log.debug("%s not found (%s)" % (self.last_job_file, os.path.exists("./last.txt")))
            lastJob = self.get_job()
            if lastJob:
                self.save_last_job_id(lastJob.id)
                return lastJob.id
            else:
                self.save_last_job_id(0)
                return 0
        else:
            try:
                f = open(self.last_job_file, 'r')
                id = int(f.readline())
                return id
            except Exception as e:
                os.remove(self.last_job_file)
                log.error("Not read %s: %s" % (self.last_job_file, e))
                return self.get_last_job_id()

    def send(self, text):
        self.send_slack(text)
        self.send_web(text)
        self.send_script(text)

    def send_script(self, text):
        if not self.result_script:
            return
        pass

    def send_web(self, text):
        if not self.web["url"]:
            return
        payload = {
            "q": text
        }
        resp = requests.get(self.web["url"], params=payload)
        if resp.status_code != 200:
            log.error("(%d): %s" % (resp.status_code, resp.text))

    def send_slack(self, text):
        if not self.slack_web_hook:
            return
        self.slack['text'] = text
        raw_data = "payload={" \
                   "\"channel\": \"%(channel)s\"," \
                   "\"username\": \"%(username)s\", " \
                   "\"text\": \"%(text)s\", " \
                   "\"icon_emoji\": \"%(icon)s\"}" % self.slack
        resp = requests.post(self.slack_url, data=raw_data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        if resp.status_code != 200:
            log.error("(%d): %s" % (resp.status_code, resp.text))

    def loop(self):
        job = self.get_job()
        log.debug("JOB: %s" % job)
        log.debug("LastJob: %s" % self.last_job)
        log.debug("Go: (%s, %s, %s) %s" %  (not job,job.id <= self.last_job,  job.ref != self.ref, (not job or job.id <= self.last_job or job.ref != self.ref)))
        if not job or job.id <= self.last_job or job.ref != self.ref:
            return
        if job.status in ["success"]:
            self.send(":arrow_forward: Found new Job (%d) ref:%s (%s)\nCreated:%s %s ```%s```" % (job.id, job.ref, job.commit['id'], job.commit['committed_date'], job.commit['author_name'], job.commit['message']) )
            self.download(job)
            self.unzip()
            self.deploy()
            self.save_last_job_id(job.id)
        elif job.status in ["created", "pending", "running"] and self.pending_job != job.id:
            self.send(":arrows_counterclockwise: new job %d" % job.id)
            self.pending_job = job.id
        elif job.status in ["failed", "canceled", "skipped"]:
            self.send(":no_entry: job %d %s" % (job.id, job.status))
            self.save_last_job_id(job.id)

    def get_job(self):
        log.debug("get-job")
        jobs = self.project.jobs.list()
        if len(jobs) > 0:
            return jobs[0]

    def download(self, job):
        log.debug("download %d" % job.id)
        target = Downloader()
        job.artifacts(streamed=True, action=target)
        del(target)  # flushes data on disk

    def unzip(self):
        log.debug("unzip artifacts.zip")
        with zipfile.ZipFile("artifacts.zip", "r") as zip_ref:
            zip_ref.extractall("./tmp")

    def deploy(self):
        log.debug("deploying script")
        pres = ""
        encoding = "utf-8"
        try:
            pres = subprocess.check_output(self.deploy_script, shell=True, stderr=subprocess.STDOUT)
            pres = str(pres, encoding)
        except subprocess.CalledProcessError as e:
            log.error(e.output)
            self.send(":sos: ./deploy.sh ```%s```" % str(e.output, encoding))
        finally:
            self.send(":white_check_mark: ./deploy.sh ```%s```" % pres)


class Downloader(object):
    def __init__(self):
        self._fd = open('artifacts.zip', 'wb')

    def __call__(self, chunk):
        self._fd.write(chunk)

