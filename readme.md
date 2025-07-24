# Content manager app for TechLabs-Printmonitor #

This app is designed to communicate with [TechLabs-Printmonitor](https://github.com/Kraakan/TechLabs-Printmonitor). Users can submit content to be shown on the monitor, and jobs for the 3D printer. Content and jobs have to be approved by an admin, and once approved it is fetched by TechLabs-Printmonitor.

## Installation

RECOMMENDED! Create a venv, and activate it:
`python3 -m venv .venv`
`source .venv/bin/activate`

To install dependencies run:
`pip install -r requirements.txt`

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
