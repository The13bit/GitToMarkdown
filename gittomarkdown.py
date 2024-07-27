import configparser
from typing import List
from git import Repo
import os
import requests
import subprocess
from concurrent.futures import ThreadPoolExecutor


from ProgressBar import ClonedProgreeBar
from Zipper import Zipper
from Generator import Generator

from Parsers import extract_git_links_xml, extract_git_links_json

from errors import SSH_key_not_set,Permission_Denied_SSH
config=configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), 'conf.cfg')
config.read(config_path)

class GitToMark:
    BASE_DIR = "./RepoStore"
    OUT_DIR = "./Output"

    def __init__(self, urls: List["str"]|str,ssh=False) -> None:
        self.ssh=ssh
        if ssh:
            if not config["Default"]["Shh_key_path"]:
                raise SSH_key_not_set
            x=subprocess.run(f'ssh -i "{config["Default"]["Shh_key_path"]}" -T git@github.com',text=False)
            if x.returncode!=1:
                raise Permission_Denied_SSH
           



        if isinstance(urls,str):
            urls=[urls]
        self.urls = []
        self.repo = []
        self.UID = [self.extract_repo_name(url,ssh) for url in urls]

        with ThreadPoolExecutor(int(config["Default"]["Threads"])) as DownloadPool:
            # self.repo=[self.Create_repo_Handle(url,i) for i,url in enumerate(self.urls)]
            for r in DownloadPool.map(
                lambda args: self.Create_repo_Handle(*args,ssh), enumerate(urls)
            ):
                if r:
                    self.repo.append(r)
    
    @classmethod
    def from_xml(cls, path):
        links = extract_git_links_xml(path)
        return cls(links)

    @classmethod
    def from_json(cls, path):
        links = extract_git_links_json(path)
        return cls(links)
    @staticmethod
    def config(threads=10,ssh_path=""):
        config["Default"]["THREADS"]=str(threads)
        config["Default"]["Shh_key_path"]=ssh_path
    @property
    def store(self):
        Zipper(self.UID)

    def extract_repo_name(self, path,ssh):
        if not ssh:
            name = path.split("/")[-2:]
            name[1] = name[1][:-4]
            name.insert(1, "-")
            name = "".join(name)
            return name
        else:
            name=path.split(":")[1].split(".")[0].split("/")
            name.insert(1,"-")
            name="".join(name)
            return name

    @property
    def generate(self):
        with ThreadPoolExecutor(int(config["Default"]["THREADS"])) as pool:
            i = 0
            for url, repo in zip(self.urls, self.repo):
                if self.ssh:
                    url=url.split(":")[1:]
                    url=''.join(url)

                Reponame = url.split("/")[-2:]
                Reponame[1] = Reponame[1][:-4]
                outfile = Reponame[1]
                Reponame.insert(1, "-")
                Reponame = "".join(Reponame)
                # pool.submit(Generator,(Reponame,repo,outfile))
                instance = Generator(Reponame, repo, outfile, i)
                pool.submit(instance.Generate_MD)
                i += 1

    def Create_repo_Handle(self, i, url,ssh):
        if os.path.exists(self.BASE_DIR + f"/{self.UID[i]}"):
            self.urls.append(url)
            return Repo(self.BASE_DIR + f"/{self.UID[i]}")
        handle = None
        if not ssh:
            if requests.get(url).status_code == 200:
                handle = Repo.clone_from(
                    url,
                    self.BASE_DIR + f"/{self.UID[i]}",
                    progress=ClonedProgreeBar(i, self.UID[i]),
                )
                self.urls.append(url)
            else:
                print(f"Invalid Url:{url}")
        else:
            handle = Repo.clone_from(
                   url,
                   self.BASE_DIR + f"/{self.UID[i]}",
                   progress=ClonedProgreeBar(i, self.UID[i]),
                   env={"GIT_SSH_COMMAND": f'ssh -i "{config["Default"]["Shh_key_path"]}"'}
               )
            self.urls.append(url)

        

        return handle
