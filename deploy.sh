#!/bin/bash

PROJECT_ID="job-interview-436117"
LOCAL_IMAGE_NAME="pybox-exec"
GCR_IMAGE_NAME="pybox-exec"
TAG="v1"
SERVICE_NAME="pybox-service"
REGION="us-central1"

# gcloud auth login
# gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable run.googleapis.com containerregistry.googleapis.com

docker build  --platform=linux/amd64  -t $LOCAL_IMAGE_NAME .

# Tag the local image
docker tag $LOCAL_IMAGE_NAME gcr.io/$PROJECT_ID/$GCR_IMAGE_NAME:$TAG

# Push the image to Google Container Registry
docker push gcr.io/$PROJECT_ID/$GCR_IMAGE_NAME:$TAG

# Deploy to Cloud Run
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$GCR_IMAGE_NAME:$TAG \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated

echo "Deployment complete.Service should now be running on Cloud Run."