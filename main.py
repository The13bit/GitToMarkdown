from git import Repo
import os
from gittomarkdown import GitToMark


# repo=Utils("https://github.com/gitpython-developers/QuickStartTutorialFiles.git")
repo = GitToMark.from_json("./Scraper/firstscrape/tmp/github.jsonl")

repo.generate
