from git import Repo
import os
from Utils import GitToMark




#repo=Utils("https://github.com/gitpython-developers/QuickStartTutorialFiles.git")
repo=GitToMark(["https://github.com/expressjs/express.git","https://github.com/gitpython-developers/QuickStartTutorialFiles.git"])

#repo.generate
repo.store
