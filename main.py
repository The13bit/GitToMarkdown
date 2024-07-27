from git import Repo
import os
from gittomarkdown import GitToMark


# repo=Utils("https://github.com/gitpython-developers/QuickStartTutorialFiles.git")
repo = GitToMark(
    [
        "https://github.com/expressjs/express.git",
        "https://github.com/gitpython-developers/QuickStartTutorialFiles.git",
        "https://github.com/am0nsec/HellsGate.git",
        "https://github.com/The13bit/Ngo-Website.git",
        "https://github.com/cvlab-stonybrook/DewarpNet.git",
        "https://github.com/krahets/hello-algo.git"
    ]
)

repo.generate
