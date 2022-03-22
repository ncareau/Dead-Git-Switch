Dead Git Switch
===

Dead man's switch using github actions scheduled daily that checks if you pushed a commit/branch on github for a configurable number of day. If the switch is triggered, the switch turns the repo public to share secret or embarassing informations. 

# Disclaimer

This project was made just for fun. I am in not way responsible for any ill advised use. Use at your own risk.

This project requires a Github Token to operate. Make sure to take correct precaution when dealing with this token as it can be used to access multiple ressources.

# How to

### Step 1 : Fork this repo.

** If you use the github fork button, you will not be able to make the repo private. Use this button only if you want to develop on this project **

In order to correctly fork this repo, you will have to create a new separate repo and mirror the project to it. 

<!-- TODO: add steps to clone -->
https://stackoverflow.com/questions/10065526/github-how-to-make-a-fork-of-public-repository-private

### Step 2 : Create Github Token


### Step 3 : Configure and Test

Fork the repo

Configure the following variables.

GH_TOKEN
DAYS

Here are the optional variables.


### Step 4 : Test the app. 

Run your application once

Change dry-run flag 

### Add payload
    
Add the information you want to make public. You can edit this readme file in order to quickly show a glance of information. 

You can link the payload ([Secret Payload](img/secret_payload.jpg)) or include it in this file :

![Luna](img/secret_payload.jpg)

