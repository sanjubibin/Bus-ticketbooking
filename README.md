# Insructions

## requirements.txt
    pip freeze > requirements.txt --> to create and update file
    pip install -r requirements.txt --> to install packages

## create a new repository on the command line
    echo "# Bus-ticketbooking" >> README.md
    git init
    git add README.md
    git commit -m "first commit"
    git branch -M main
    git remote add origin https://github.com/sanjubibin/Bus-ticketbooking.git
    git push -u origin main

## push an existing repository from the command line
    git remote add origin https://github.com/sanjubibin/Bus-ticketbooking.git
    git branch -M main
    git push -u origin main

## push all the project code in the main branch of GitHub
    # Check the current branch
    git status

    # Add all the files in the current directory to the staging area
    git add .

    # Commit the changes to the staging area
    git commit -m "Pushing all the project code to GitHub"

    # Push the changes to the main branch on GitHub
    git push origin main

## git clone
    git clone <git repository url>

## things to edit in env folder 
### path --> <env name>/lib/python3.10/site-packages/swagger_ui/views.py
    change this in line 10 of
        spec = yaml.load(file.read())
    to 
        spec = yaml.load(file.read(), Loader=yaml.Loader)
### path --> <env name>/lib/python3.10/site-packages/swagger_ui/templates/swagger_base.html
    change the line 1 of
        {% load staticfiles %}
    to 
        {% load static %}
### path --> <env name>/lib/python3.10/site-packages/swagger_ui/apps.py
    change the line 5 of
        name = 'yaml_converter'
    to 
        name = 'swagger_ui'






