from hashlib import sha256
from typing import List
from git import Repo
import os
import requests
from concurrent.futures import ThreadPoolExecutor
import wget
from MarkdownUtils import Markdown
from ProgressBar import ClonedProgreeBar
from Zipper import Zipper
from Generator import Generator


class GitToMark:
    BASE_DIR = "./RepoStore"
    OUT_DIR = "./Output"

    def __init__(self, urls: List["str"]) -> None:
        self.urls = []
        self.repo = []
        self.UID = [self.generate_random_file_string(url) for url in urls]

        with ThreadPoolExecutor(10) as DownloadPool:
            # self.repo=[self.Create_repo_Handle(url,i) for i,url in enumerate(self.urls)]
            for r in DownloadPool.map(
                lambda args: self.Create_repo_Handle(*args), enumerate(urls)
            ):
                if r:
                    self.repo.append(r)

    @property
    def store(self):
        Zipper(self.UID)

    def generate_random_file_string(self, path):
        name = path.split("/")[-2:]
        name[1] = name[1][:-4]
        name.insert(1, "-")
        name = "".join(name)
        return name

    @property
    def generate(self):
        with ThreadPoolExecutor(2) as pool:
            i = 0
            for url, repo in zip(self.urls, self.repo):
                Reponame = url.split("/")[-2:]
                Reponame[1] = Reponame[1][:-4]
                outfile = Reponame[1]
                Reponame.insert(1, "-")
                Reponame = "".join(Reponame)
                # pool.submit(Generator,(Reponame,repo,outfile))
                instance = Generator(Reponame, repo, outfile, i)
                pool.submit(instance.Generate_MD)
                i += 1

    def Create_repo_Handle(self, i, url):
        if os.path.exists(self.BASE_DIR + f"/{self.UID[i]}"):
            self.urls.append(url)
            return Repo(self.BASE_DIR + f"/{self.UID[i]}")
        handle = None
        if requests.get(url).status_code == 200:
            handle = Repo.clone_from(
                url,
                self.BASE_DIR + f"/{self.UID[i]}",
                progress=ClonedProgreeBar(i, self.UID[i]),
            )
            self.urls.append(url)
        else:
            print(f"Invalid Url:{url}")
        return handle
