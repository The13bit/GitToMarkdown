from git import Repo
import os
from GitToMarkDown import GitToMark

GitToMark.config(10,"C:\\Users\\anasf\\.ssh\\github")

# repo=Utils("https://github.com/gitpython-developers/QuickStartTutorialFiles.git")
repo = GitToMark("git@github.com:nopnop2002/esp-idf-w25q64.git",True)

repo.generate
