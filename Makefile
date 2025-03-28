#########
### DOCKER LOCAL
#########

include .env


build_container_local:
	docker build --tag=${IMAGE}:dev .

run_container_local: build_container_local
	docker run -it -e PORT=${PORT} -v ./package_folder:/app/package_folder -p ${PORT}:${PORT} ${IMAGE}:dev

#########
## DOCKER DEPLOYMENT
#########

# Step 1 ( ONLY FIRST TIME)
allow_docker_push:
	gcloud auth configure-docker ${GCP_REGION}-docker.pkg.dev

# Step 2 ( ONLY FIRST TIME)
create_artifacts_repo:
	gcloud artifacts repositories create ${GCP_PROJECT} --repository-format=docker --location=${GCP_REGION} --description="Repository for storing images"

# Step 3
build_for_production:
	docker build -t  ${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/${IMAGE}:prod .

### Step 3 (⚠️ M1 M2 M3 M4 SPECIFICALLY)
m_chip_build_image_production:
	docker build --platform linux/amd64 -t ${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/${GCP_REPOSITORY}/${IMAGE}:prod .

## Step 4
push_image_production:
	docker push ${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/${GCP_REPOSITORY}/${IMAGE}:prod

# Step 5
deploy:
	gcloud run deploy --image ${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/${GCP_REPOSITORY}/${IMAGE}:prod --memory ${GAR_MEMORY} --region ${GCP_REGION} --timeout=600 --cpu 2 ${GCP_SERVICE_NAME} --allow-unauthenticated

undeploy:
	gcloud run services delete ${GCP_SERVICE_NAME} --region=${GCP_REGION}

build_deploy_mac: m_chip_build_image_production push_image_production deploy

build_deploy: build_for_production push_image_production deploy

# Disabling the Service
# Adjust the service's configuration to scale down to zero instances.
# This way, no resources will be used, and you won't incur charges for active instances.
cloud_run_disable_service:
	gcloud run services update ${INSTANCE} --min-instances=0

# Delete the Service
cloud_run_delete_service:
	gcloud run services delete $$INSTANCE

run_movie_search:
	python -c 'from semantic_search.interface.movie_search import search_similar_movies; search_similar_movies("batman", "../preprocessed_data/movies_with_tokenized_plots.csv")'
