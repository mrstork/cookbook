pre-deploy:
	./manage.py collectstatic --no-input
deploy:
	./google-cloud-sdk/bin/gcloud app deploy
dbshell:
	./cloud_sql_proxy -instances="ryorisho:us-central1:ryorisho-mysql"=tcp:3306
tail:
	./google-cloud-sdk/bin/gcloud app logs tail -s default
