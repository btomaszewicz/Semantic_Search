This the README file of the Semantic_Search Team

##DEPLOYING & UPDATES TO THE SEMANTIC SEARCH API
-- #Prerequisites
*Docker installed and running on your local machine
*Google Cloud SDK (gcloud) installed and configured
*Access to the semantic-search-454114 GCP project

#STEP 1: BUILD & PUSH THE DOCKER IMAGE
1. Build the Docker image with an appropriate version tag = Replace VERSION with an appropriate version number (e.g., 1.0, 1.1):
- For Intel/AMD machines (Windows, Linux, or Intel-based Macs):
docker build -t europe-west1-docker.pkg.dev/semantic-search-454114/semantic-search/semantic_search_mvp:VERSION .
- For Apple Silicon Macs (M1/M2/M3):
docker build --platform linux/amd64 -t europe-west1-docker.pkg.dev/semantic-search-454114/semantic-search/semantic_search_mvp:VERSION .

2. Push the image to Google Artifact Registry:
docker push europe-west1-docker.pkg.dev/semantic-search-454114/semantic-search/semantic_search_mvp:VERSION

#STEP 2: DEPLOY to CLOUD RUN
1. Deploy the new image to Cloud Run:
gcloud run deploy semanticsearchmvp \
  --image europe-west1-docker.pkg.dev/semantic-search-454114/semantic-search/semantic_search_mvp:VERSION \
  --region europe-west1 \
  --platform managed

2. Wait for the deployment to complete. The command will output the URL of your service, which will remain unchanged: https://semanticsearchmvp-4789051693.europe-west1.run.app/
