# Ryōrisho

A recipe sharing site - a side project of mine combining several of my hobbies.

The starting point for this project was the following repository:
https://github.com/openshift-quickstart/django-example

Thank you to everyone who contributed to that repository. It was extremely useful in getting started and taught me so much.

### Getting started

Install the RHC client tools if you don't have them yet

  ```
  sudo gem install rhc
  rhc setup
  ```

Set up the application

  ```
  rhc app create APP_NAME python-3.3 --from-code GIT_URL
  rhc ssh APP_NAME
  python $OPENSHIFT_REPO_DIR/wsgi/cookbook/manage.py createsuperuser
  ```

The app should now be available at

  ```
  http://APP_NAME-$yournamespace.rhcloud.com/admin/
  ```

For local development I advise working in a virtual environment so that you can match the server versions of all the dependencies. You likely do not have Python 3.3 installed, so you will have to start by doing that, then following the steps below.

  ```
  virtualenv -p /path/to/python3.3 venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```
