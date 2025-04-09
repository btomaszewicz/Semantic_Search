# Prerequisites
* Docker installed and running on your local machine
* Google Cloud SDK (gcloud) installed and configured
* (Access to the wagon-bootcamp-452110 GCP project for deploying)

# Setup
Copy .env.example to .env
```sh
cp .env.example .env
```
Generate the models running the Jupyter Notebook [Generate models for the search function](notebooks/am_movies_models.ipynb)

# Run Locally


To build and run the app locally, run `make run_container_local` in shell. You'll be able to access the streamlit front-end at http://localhost:8501. Everything will be updated when you save your changes to the code.

Streamlit in `package_folder/frontend.py` handles both retrieving data from the `semantic_search` module and displaying it the browser.

```sh
make run_container_local
```


# Deploy
To build and deploy the image to production, you need to run the following command if you are using a non mac computer:
```sh
make build_deploy
```
If you are using a mac with M1, M2, M3 chips, you need to run this instead:
```sh
make build_deploy_mac
```
