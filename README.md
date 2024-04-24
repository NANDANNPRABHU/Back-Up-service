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
run
docker build -t back-up-service:latest . 
in terminal







docker run command
``` docker run -p 8080:80 -ti --rm -v "A:/6th sem/CC/miniproject/Back-Up-service/backup:/usr/src/app/files" back-up-service ```

