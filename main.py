#!/usr/bin/python

import sys, os, time, json, re
from datetime import datetime

# COLORS
x = '\33[m' # DEFAULT
k = '\033[93m' # KUNING
kk = '\033[33m' # KUNING
h = '\x1b[1;92m' # HIJAU
hh = '\033[32m' # HIJAU
u = '\033[95m' # UNGU
b = '\33[1;96m' # BIRU
p = '\x1b[0;34m' # BIRU


PWD = os.getcwd()
pathfiles = f"{ PWD }/.autogit"
GIT_FOLDER = f"{ PWD }/.git"
GIT_USERNAME = ""
GIT_TOKEN = ""
GIT_EMAIL = ""
GIT_REMOTE = ""
GIT_CREDENTIALS = []

DEFAULT_GITIGNORE = f"""
/node_modules
/public/hot
/public/storage
/storage/*.key
/vendor
/__pycache__
.env
.env.backup
.phpunit.result.cache
docker-compose.override.yml
Homestead.json
Homestead.yaml
npm-debug.log
yarn-error.log
/.idea
/.vscode

# autogit config
/{ os.path.basename(pathfiles) }
"""

def clear():
    os.system('clear')
def now():
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")
def warn(text):
    print(f"{ x }[{ k }*{ x }] { text }")
def inputText(text):
    return input(f'{ x }[{ b }<>{ x }] { text } : ')
def success(text):
    print(f"{ x } [{ h }•{ x }] { text }")
def info(text):
    print(f"{ x }[{ b }!{ x }] { text }")
def question(text):
    i = input(f"{ x }[{ u }?{ x }] { text } (y/n):")
    if i in ["y", "yes"]:
        return True
    elif i in ["n", "no"]:
        return False
    else:
        warn("invalid answer !")
        question(text)

def pathExist(path):
    return os.path.exists(f"{ path }")
    
def initialize():
    global GIT_FOLDER, GIT_EMAIL, GIT_TOKEN, GIT_REMOTE, GIT_USERNAME, GIT_CREDENTIALS, DEFAULT_GITIGNORE, pathfiles
    
    if pathExist(f"{ PWD }/.gitignore"):
        with open(f"{ PWD }/.gitignore", "r") as file:
            content = file.read()
            if not re.search("autogit", content):
                with open(f"{ PWD }/.gitignore", "w") as f:
                    f.write(DEFAULT_GITIGNORE)
                    f.close()
                    info("generate file .gitignore")
            file.close()
    else:
        with open(f"{ PWD }/.gitignore", "w") as file:
            file.write(DEFAULT_GITIGNORE)
            file.close()
            info("generate file .gitignore")
            
    if pathExist(f"{ pathfiles }/creadentials.json"):
        info("creadentials found using it !")
        with open(f"{ pathfiles }/creadentials.json") as file:
            GIT_CREDENTIALS = json.loads(file.read())
            GIT_EMAIL = GIT_CREDENTIALS["data"]["email"]
            GIT_USERNAME = GIT_CREDENTIALS["data"]["username"]
            GIT_TOKEN = GIT_CREDENTIALS["data"]["token"]
            GIT_REMOTE = GIT_CREDENTIALS["data"]["remote"]
            GIT_FOLDER = GIT_CREDENTIALS["data"]["path"]
            file.close()
    else:
                
        GIT_USERNAME = inputText("input your username")
        GIT_EMAIL = inputText("input your email")
        GIT_TOKEN = inputText("input your token")
        GIT_REMOTE = inputText("input git remote")
        
        # add remote
        os.system(f"git remote add { inputText('remote name') } { GIT_REMOTE }")
        
        CREDENTIALS = json.dumps({
          "datetime": now(),
          "data": {
            "username": GIT_USERNAME,
            "email": GIT_EMAIL,
            "token": GIT_TOKEN,
            "remote": GIT_REMOTE,
            "path": GIT_FOLDER
          }
        })
        
        if question("save the git creadentials ?"):
            with open(f"{ pathfiles }/creadentials.json", 'w') as file:
                  file.write(CREDENTIALS)
                  file.close()
        else:
            warn("creadentials not saved!")
            
        GIT_CREDENTIALS = json.loads(CREDENTIALS)
    return GIT_CREDENTIALS
    
def main():
    global GIT_FOLDER, pathfiles
    if not pathExist(GIT_FOLDER):
        os.system("git init")
        info("initialize empty git")
    else:
        info("git exist, nothing to re-initialize !")
    
    if not pathExist(pathfiles):
        # create folder
        os.makedirs(pathfiles)
        
    CREADENTIALS = initialize()
    email = CREADENTIALS['data']['email']
    username = CREADENTIALS['data']['username']
    token = CREADENTIALS['data']['token']
    remote = CREADENTIALS['data']['remote']
    
    os.system(f'git config user.email "{ email }"')
    os.system(f'git config user.name "{ username }"')
    
    os.system(f"git checkout { inputText('branch name') }")
    os.system(f"git add { inputText('file to commit') }")
    os.system(f"git commit -m { inputText('commit message') }")
    
    if question("you want to push this repository ?"):
        info(f"your username is { h }{ username }{ x }")
        info(f"your token is { k }{ token }{ x }")
            
        os.system(f"git push { inputText('remote name') } { inputText('branch name') } ")
    else:
        info("exiting without push repository !")
        exit()
        
# main
main()