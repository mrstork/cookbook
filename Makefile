# help:
# 	cat Makefile | grep -E '^[a-zA-Z_-]+:.*?## .*$$' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
db_backup:
	./manage.py dumpdata --exclude auth.permission --exclude contenttypes > backup.json
