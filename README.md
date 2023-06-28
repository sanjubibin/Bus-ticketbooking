# Insructions

## requirements.txt
    pip freeze > requirements.txt --> to create and update file
    pip install -r requirements.txt --> to install packages

## get step by step for push
    git init
    git add .
    git commit -m "commit name"
    git remote add origin <git repository url>
    git push <git repository url>

## git instructions
    git init --> for initial working
    git add . --> for every change in project(check this)
    git status --> to check whether there are any changes made for commiting
    git commit -m "commit name" --> when ever needed for commiting
    git push 
    git remote add <name> <url> --> name-sanjubibin, url-https://github.com/sanjubibin/git-testing.git
    git pull <url> --> to make changes to the local project folder with exact folder in github repository

## git clone
    git clone <git repository url>

## things to edit in env folder 
### path --> <env name>/lib/python3.10/site-packages/swagger_ui/views.py
    change this in line 10 of
        spec = yaml.load(file.read())
    to 
        spec = yaml.load(file.read(), Loader=yaml.Loader)
### path --> <env name>/lib/python3.10/site-packages/swagger_ui/swagger_base.html
    change the line 1 of
        {% load staticfiles %}
    to 
        {% load static %}
### path --> <env name>/lib/python3.10/site-packages/swagger_ui/apps.py
    change the line 5 of
        name = 'yaml_converter'
    to 
        name = 'swagger_ui'






