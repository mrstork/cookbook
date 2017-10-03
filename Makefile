pre-deploy:
	./manage.py collectstatic --no-input
deploy:
	./google-cloud-sdk/bin/gcloud app deploy
dbshell:
	./cloud_sql_proxy -instances="ryorisho-app:us-central1:ryorisho-mysql"=tcp:3306
tail:
	./google-cloud-sdk/bin/gcloud app logs tail -s default
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
