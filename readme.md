# Content manager app for TechLabs-Printmonitor #

This app is designed to communicate with [TechLabs-Printmonitor](https://github.com/Kraakan/TechLabs-Printmonitor). Users can submit content to be shown on the monitor, and jobs for the 3D printer. Content and jobs have to be approved by an admin, and once approved it is fetched by TechLabs-Printmonitor.

## Installation

> [!NOTE]
> This app requires Python 3.11. 
>
> If you are running another version of python on your system you can easily get this app to run 3.11 using pyenv:
> ```
> curl -fsSL https://pyenv.run | bash
> export PYENV_ROOT="$HOME/.pyenv"
> [[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
> eval "$(pyenv init - bash)"
> pyenv install 3.11
> pyenv global 3.11
> ```

Then, proceed with creating and activating a venv with python 3.11 
```
python3 -m venv venv
source venv/bin/activate 
```

Continue by installing the dependencies
``` 
pip install -r requirements.txt 
```


Install and deploy TechLabs-Printmonitor by following isntructions at:
[`https://github.com/Kraakan/TechLabs-Printmonitor`](https://github.com/Kraakan/TechLabs-Printmonitor)

## Deployment

`flask --app . run`

> [!NOTE]
> `.env` file is required, containing the following secrets:
>```
> ADMIN_USERNAME=YOUR_USERNAME 
> ADMIN_PASSWORD=YOUR_PASSWORD
>```

If you deployed TechLabs-Printmonitor before starting this app and uploading content, your approved content will be fetched in a minute or so.

# Endpoints

## All users
/

### Memes

#### List memes
/memes/

#### Submit meme (for validation by admin)
/memes/submit/

### 3D printing

#### List jobs
/3dprint/

#### Submit print job (for validation by admin)
/3dprint/submit/

## admin

### Login
/manage/login

### Logout
/logout

### Manage submitted print jobs
/manage/3dprint/

### Manage submitted memes
/manage/memes/

## apis
These are meant to be accessed by TechLabs-Printmonitor

### Get meme data
/api/memes/

### Get print job data
/api/jobs/
