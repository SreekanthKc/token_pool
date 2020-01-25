pip install  -r requirements.txt
python main.py
http://localhost:8080

gcloud app deploy app.yaml --project jupiter-app --version uat --no-promote

gcloud app deploy index.yaml --project jupiter-app

##set cors policy on upload bucket
gsutil cors set /home/lijo/Projects/jupiter-app/cors.txt gs://csv_uploads_0909
##verify cors
curl -v -X OPTIONS -H "Host: storage.googleapis.com" -H "Access-Control-Request-Method: PUT"  -H "Origin: http://localhost:3000" "https://storage.googleapis.com/test_large_files_3456/cors.txt"

###For download csv files - using IAM roles, to make the files readable, and block listing:
```
gsutil iam ch allUsers:legacyObjectReader gs://jupiter_csv_uploads/
```
To set env variables while running the app locally: 
execute /home/lijo/Projects/api-gateway/jupiter-app/env/env.txt

gcloud beta functions deploy jupiter_callback_for_rac --env-vars-file .env.yaml --memory=2048MB --timeout=540s --runtime python37 --trigger-http

gcloud beta functions deploy send_to_gateway --memory=2048MB --env-vars-file .env.yaml --timeout=540s --runtime python37 --trigger-resource chunk_json_staging_5678 --trigger-event google.storage.object.finalize

###Cloud function: Calculate count of keywords of a specific user and store to Datastore. Triggered by keyword-counter Cloud Task
```
gcloud beta functions deploy keyword_counter --memory=2048MB --timeout=540s --runtime python37 --trigger-http
```

bq show --schema --format=prettyjson jupiter-app:Master.datalake_test
