# Back-Up-service
Back Up service using docker and Kubernetes

download credentials.json from console.cloud.google.com google-drive api
for refference yotube video link is given below
https://youtu.be/G_4KUbuwtlM?si=U29qsiWeuLTLFhai


next step


in docker-compose.yml file
services:
  back-up-service:
    image: back-up-service:latest
    volumes:
      - A:/6th sem/CC/miniproject/Back-Up-service/backup:/usr/src/app/files
change path to your directory which will be getting backup service
and followed by :/usr/src/app/files

next step


run the get_token.py to get authorised


next step

create a folder in mydrive of your google-drive
run the get_folder_id.py
and type your folder name as input and press enter
.env file will be created in your path


nextstep

run docker in your system


run
docker build -t back-up-service:latest . 
in terminal

next step 

run
docker compose up


now u can do modification in the folder which is A:/6th sem/CC/miniproject/Back-Up-service/backup in my case

add some file and delete file

the changes will be reflected in your drive folder







# Back-Up Service

This guide outlines how to set up and run a backup service using Docker and Kubernetes, which automatically syncs your designated local folder to Google Drive.

## Prerequisites

- Docker installed on your machine.
- Kubernetes cluster (optional, if scaling is required).
- Google Cloud account to access Google Drive API.

## Step 1: Google Drive API Credentials

1. Obtain `credentials.json` for the Google Drive API from [Google Cloud Console](https://console.cloud.google.com/).
2. Download the credentials file and save it to your project directory.

For assistance, refer to this YouTube tutorial: [Setting Up Google Drive API](https://youtu.be/G_4KUbuwtlM?si=U29qsiWeuLTLFhai)

## Step 2: Configure Docker

Edit the `docker-compose.yml` file to specify the path to your local directory that you want to back up:

```yaml
services:
  back-up-service:
    image: back-up-service:latest
    volumes:
      - /path/to/your/directory:/usr/src/app/files
```


### Step 3: Authorization

Run the `get_token.py` script to get authorized with Google.

### Step 4: Create Google Drive Folder

- Create a folder in your Google Drive to store the backups.
- Run the `get_folder_id.py`, enter your folder name to get the folder ID, and generate `.env` file with the folder ID.

### Step 5: Build Docker Image

Execute the following command to build the Docker image:

```bash
docker build -t back-up-service:latest .
```

### Step 6: Launch the Service

Start the service using Docker Compose:

```bash
docker compose up
```


### Step 7: Modify the Local Folder

Make changes (add or delete files) in the local backup directory specified in Step 2. These changes will be synchronized to your Google Drive folder.


