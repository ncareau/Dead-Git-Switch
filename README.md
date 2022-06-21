Dead Git Switch
===

Dead man's switch using GitHub actions scheduled daily that checks if you pushed a commit/branch on GitHub for a configurable number of days. If the switch is triggered, the script turns the repo public to share secrets or embarrassing information to encourage maintaining regular coding habits.

# Disclaimer

This project was made just for fun. I am in no way responsible for any ill-advised use. Use at your own risk.

⚠ This project requires a Github Personal Token to operate. ⚠ Make sure to take the correct precautions when dealing with this token as it can be used to access multiple resources.

# How to

### Step 1 : Import DeadGitSwitch in new private repo

> ⚠ Important! If you use GitHub fork, you will not be able to make the repo private. Use this button only if you want to contribute on this project.

In order to correctly fork this repo, you will have to create a new private repo and import the project to it. This is also the most secure option because only you have access/knowledge of that repo. 

In GitHub, click `+` next to your username and then: `Import repository`

![GithubImport](img/github-import.png)

Use this repo URL : `https://github.com/ncareau/dead-git-switch`

Add a name and select **Private** privacy.

### Step 2 : Create Github Token

A GitHub token can be created at https://github.com/settings/tokens

Under Settings -> Developer settings -> Personal access tokens

Create the token with `No Expiration` and `repo` (all) + `read:user` scopes.

### Step 3 : Configure

Configure the following variables.

Add the following Github Actions Secrets location in your project `Settings` -> `Secrets` -> `Actions` menu.

| Variable     | Description |
| ----------- | ----------- |
| **GH_TOKEN**      | **Required** - Github token generated in Step 2 |
| **DRY_RUN** | **Required** - Default to `True`. Test until you have a working script then change to `False` to arm. |

Modify the `.env` with your preference. 

| Variable     | Description |
| ----------- | ----------- |
| **DAYS**   | **Required** - Number of days of commit inactivity until it triggers the switch. |
| **GH_PUBLIC_ONLY**   | If the script should look in your public commits only. If `False`, will look for private and public commits. |
| **RETURN_PRIVATE**   | If the script should make the project private again after a recent commit. |

> Variables in `.env` takes precedence to variables in Github Actions Secrets. Comment the line in `.env` if you want to override it in Github Actions Secrets.

### Step 4 : Test 

Run your application in dry _run mode in order to check if everything runs correctly.

Look for LAST_DRY_RUN in your GitHub actions secrets to confirm that the script ran successfully. 

Once you confirmed that the script ran once successfully, you can change `DRY_RUN` to `False` to arm the script correctly. 

### Step 5 : Add payload
    
Add the information you want to make public to this repository. You can edit this readme file in order to quickly show a glance of information. Or change it completely to add your information. You could add embarrassing pictures to encourage maintaining regular coding habits.

You can link the payload ([Secret Payload](img/secret_payload.jpg)) or modify this readme.md file to include your files :

![Luna](img/secret_payload.jpg)
