# Content manager app for TechLabs-Printmonitor #

This app is designed to communicate with TechLabs-Printmonitor. Users can submit content to be shown on the monitor, and jobs for the 3D printer. Content and jobs that have been approved by an admin is fetched by TechLabs-Printmonitor (fork).

## Installation

To install dependencies run:
pip intall -r requirements.txt

## Deployment

> [!NOTE]
> `.env` file is required, containing the following secrets:
>```
> ADMIN_USERNAME=YOUR_USERNAME 
> ADMIN_PASSWORD=YOUR_PASSWORD
>```

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