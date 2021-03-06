import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

from base64 import b64encode
from nacl import encoding, public

from ghapi.all import GhApi, date2gh, gh2date, actions_warn, actions_error

load_dotenv(override=True)

# Function to encrypt variable for GitHub secrets.
def encrypt(public_key: str, secret_value: str) -> str:
    """Encrypt a Unicode string using the public key."""
    public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return b64encode(encrypted).decode("utf-8")


# Load env_var and secrets
gh_token = os.getenv("GH_TOKEN")
gh_repo = os.getenv("GH_REPOSITORY")
gh_public_only = os.getenv("GH_PUBLIC_ONLY")  # Bool
days = os.getenv("DAYS")
dry_run = os.getenv("DRY_RUN")  # Bool
return_private = os.getenv("RETURN_PRIVATE")  # Bool
last_run = os.getenv("LAST_RUN")
last_dry_run = os.getenv("LAST_DRY_RUN")
last_pushed_id = os.getenv("LAST_PUSHED_ID")
last_pushed_date = os.getenv("LAST_PUSHED_DATE")

# We get the owner and repo separately for calling the API.
owner = gh_repo.split(sep="/")[0]
repo = gh_repo.split(sep="/")[1]

# We make sure we are running dry unless we are ready.
if dry_run in ["True", "true", True]:
    dry_run = True
else :
    dry_run = False

switch_trigger = False

print("")
print("  ____                 _         _ _                  _ _       _     ")
print(" |  _ \  ___  __ _  __| |   __ _(_) |_   _____      _(_) |_ ___| |__  ")
print(" | | | |/ _ \/ _` |/ _` |  / _` | | __| / __\ \ /\ / / | __/ __| '_ \ ")
print(" | |_| |  __/ (_| | (_| | | (_| | | |_  \__ \\\\ V  V /| | || (__| | | |")
print(" |____/ \___|\__,_|\__,_|  \__, |_|\__| |___/ \_/\_/ |_|\__\___|_| |_|")
print("                           |___/                                      ")
print("             By NMC - github.com/ncareau/dead-git-switch              ")
print("")
print("")


# We check that we have the minimal environmental variables.
if gh_token == "":
    print("ERROR: You are missing the required Github Actions secret named: GH_TOKEN")
    exit(1)

if days == "":
    print("ERROR: You are missing the required Github Actions secret named: DAYS")
    exit(1)


# Display some variables for debugging.
print("Repo:                  " + gh_repo)
print("Dry run:               " + ("Yes" if dry_run else "No"))
print("Days:                  " + days) # Verify this value in dry_run mode
print("Last run:              " + (gh2date(last_run).isoformat() if last_run else "Never")) # We use UTC time to sync with GitHub
print("Last dry run:          " + (gh2date(last_dry_run).isoformat() if last_dry_run else "Never")) 
print("Last pushed date:      " + (gh2date(last_pushed_date).isoformat() if last_pushed_date else "Never"))
print("")
print("")

# Connection to Github API.
# Owner and repo will make sure all actions will be done on this repository only. 
g = GhApi(token=gh_token, owner=owner, repo=repo)

# Get more info on the current repository.
# repo_info = g.repos.get()
# print(repo_info.private)

if gh_public_only in ['True', 'true', True]:
    # Get all public events.
    user_events = g.activity.list_public_events_for_user(username=owner, per_page=100)
else:
    # Get all events, private and public.
    user_events = g.activity.list_events_for_authenticated_user(username=owner, per_page=100)  

# To encrypt secrets, we need the repo public key.
pub_key = g.actions.get_repo_public_key()

# Look for pushed commit action (PushEvent and CreateEvent)
# We assume the that the first event we see is the latest one.
for activity in user_events:
    if activity.type == "PushEvent" or activity.type == "CreateEvent":
        last_pushed_commit = activity
        break

# New commit found, update last_pushed_commit
if last_pushed_id != last_pushed_commit.id:
    print("** New commit found **")
    print("ID: "+last_pushed_commit.id+"   -   Date: "+last_pushed_commit.created_at)
    print("")
    g.actions.create_or_update_repo_secret(secret_name="LAST_PUSHED_ID", encrypted_value=encrypt(public_key=pub_key.key, secret_value=last_pushed_commit.id), key_id=pub_key.key_id)
    g.actions.create_or_update_repo_secret(secret_name="LAST_PUSHED_DATE", encrypted_value=encrypt(public_key=pub_key.key, secret_value=last_pushed_commit.created_at), key_id=pub_key.key_id)

# Get the difference between
dif = datetime.utcnow() - gh2date(last_pushed_commit.created_at)

print("Time since last commit: " + str(dif))

# Check if the switch should be triggered. 
if dif > timedelta(days=int(days)):

    # Switch Triggered.
    print("Switch triggered !!")
    switch_trigger = True

    if dry_run is False:
        # Do action. In this case, make the repo public. 
        # This is where you can modify to run any actions when the switch is triggered. 
        print("Making repository public.")
        g.repos.update(private=False)
    else:
        print("DryRun enabled, no change was made.")
else:
    # We are under the trigger limit
    print("Under the trigger limit")

    # Warn if the switch will trigger in less than 3 days
    if timedelta(days=int(days)) - dif < timedelta(days=3):
        actions_warn("The switch will be activated in less than 3 days.")

    # Verify if we should change the repo back to private.
    if return_private in ['True', 'true', True] and not g.repos.get().private:
        if dry_run is False:
            print("Returning Repository to private.")
            g.repos.update(private=True)
        else:
            print("DryRun enabled, didn't return repository to private.")    


# Success - Record end of script time.
print("SUCCESS - The script ran correctly. We will record the time")

last_run_datetime = date2gh(datetime.utcnow())

if dry_run is False:
    print("LAST_RUN : " + last_run_datetime)
    g.actions.create_or_update_repo_secret(
        secret_name="LAST_RUN",
        encrypted_value=encrypt(public_key=pub_key.key, secret_value=last_run_datetime),
        key_id=pub_key.key_id
    )
else:
    print("LAST_DRY_RUN : " + last_run_datetime)
    g.actions.create_or_update_repo_secret(
        secret_name="LAST_DRY_RUN",
        encrypted_value=encrypt(public_key=pub_key.key, secret_value=last_run_datetime),
        key_id=pub_key.key_id
    )


# Fail GitHub action if the switch triggered to notify the user. 
if switch_trigger:
    actions_error("Switch triggered ! - Returning error to notify user.")
    raise SystemExit()
