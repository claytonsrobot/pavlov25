#**Build the Docker Image**:
docker build -t my-webapp .
#**Run the Docker Container**:
docker run -d -p 80:80 my-webapp