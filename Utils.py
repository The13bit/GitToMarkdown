from hashlib import sha256
from typing import List
from git import Repo
import os

from MarkdownUtils import Markdown
from ProgressBar import ClonedProgreeBar

from sys import stdout

class Generator:
    BASE_DIR="./RepoStore"
    OUT_DIR="./Output"
    def __init__(self,reponame:str,repo:Repo,outfile:str) :
        self.repoName=reponame
        self.repo=repo
        self.tree=repo.head.commit.tree
        self.MDout="./"+self.OUT_DIR+"/"+outfile+".md"
        self.MD=Markdown(self.MDout)
        self.total=0
        self.dirs=0
        
        
    def print_files_from_git(self,root, level=0):
     for entry in root:
         #print(f'{"-" * 4 * level}| {entry.path}, {entry.type}')
         self.total+=1
         
         tmp=f'{" "*level*2}- {entry.path}'+"\n"
        
         yield tmp
         if entry.type == "tree":
             self.dirs+=1
             yield from self.print_files_from_git(entry, level + 1)

    
    
    def write_files_in_MD(self,root,level=0):
        for entry in root:
            if entry.type=="tree":
                self.write_files_in_MD(entry,level+1)
            else:
                self.MD.add_header(entry.path,2)
                with open(self.BASE_DIR+'/'+self.repoName+'/'+entry.path,"r",encoding='utf-8') as f:
                    x=entry.path.split('.')[-1]
                    if x.lower()!="md":

                        self.MD.add_code_block(f.read(),x)
    
    def write_git_tree(self):
        self.MD.add_header("Git Tree",2)
        for line in self.print_files_from_git(self.tree):
            stdout.write(f"\rFiles:{self.total-self.dirs}|Dirs:{self.dirs}")
            stdout.flush()
            self.MD.add_para(line)

                
    def write_header(self):
        
        #split=self.urls.split('/')[-2:]
        #split.insert(1,"/")
        #
        #Headinfo=''.join(split)[:-4]
        self.MD.add_header(self.repoName.replace('-',"/"))
    

    @property
    def Generate_MD(self):
        self.write_header()
        self.write_git_tree()
        self.write_files_in_MD(self.tree)
    def print_tree(self):
        self.print_files_from_git(self.tree)


class GitToMark:
    BASE_DIR="./RepoStore"
    OUT_DIR="./Output"
    def __init__(self,urls:List["str"]) -> None:
        self.urls=urls
        self.UID=[self.generate_random_file_string(url) for url in self.urls]
        self.repo=[self.Create_repo_Handle(url,i) for i,url in enumerate(self.urls)]
        
   
        
    
    
    def generate_random_file_string(self,path):
        name=path.split("/")[-2:]
        name[1]=name[1][:-4]
        name.insert(1,"-")
        name=''.join(name)
        return name

    
    @property
    def generate(self):
        for url,repo in zip(self.urls,self.repo):
            Reponame=url.split("/")[-2:]
            Reponame[1]=Reponame[1][:-4]
            outfile=Reponame[1]
            Reponame.insert(1,"-")
            Reponame=''.join(Reponame)
            Generator(Reponame,repo,outfile).Generate_MD


    def Create_repo_Handle(self,url,i):
        if os.path.exists(self.BASE_DIR+f"/{self.UID[i]}"):
            return Repo(self.BASE_DIR+f"/{self.UID[i]}")
        
        handle=Repo.clone_from(url,self.BASE_DIR+f"/{self.UID[i]}",progress=ClonedProgreeBar())
        return handle
 
    
        
