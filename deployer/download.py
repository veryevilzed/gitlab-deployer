#coding:utf-8
import gitlab, logging, zipfile, requests, os

from .deployer import Downloader

log = logging.getLogger("DOWNLOADER")


class Download:
    def __init__(self, url, private_token, project_id, ref):
        self.gl = gitlab.Gitlab(url, private_token, api_version=4)
        self.project = self.gl.projects.get(project_id)
        self.get_job(ref)

    def get_job(self, ref):
        log.debug("get-job:%s" % ref)
        jobs = self.project.jobs.list()
        for job in jobs:
            if job.ref == ref:
                self.download(job)
                self.unzip()
                break

    def download(self, job):
        log.debug("download %d" % job.id)
        target = Downloader()
        job.artifacts(streamed=True, action=target)
        del(target)

    def unzip(self):
        log.debug("unzip artifacts.zip")
        with zipfile.ZipFile("artifacts.zip", "r") as zip_ref:
            zip_ref.extractall("./")
        os.remove("artifacts.zip")

