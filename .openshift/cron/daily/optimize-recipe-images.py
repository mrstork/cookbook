import os
from PIL import Image

CRON_DAILY_DIR = os.path.dirname(os.path.abspath(__file__))
CRON_DIR = os.path.dirname(CRON_DAILY_DIR)
OPENSHIFT_DIR = os.path.dirname(CRON_DIR)
REPO_DIR = os.path.dirname(OPENSHIFT_DIR)

recipe_images_directory = os.path.join(REPO_DIR, 'wsgi', 'static', 'media','recipe-images')

for filename in os.listdir(recipe_images_directory):
    absolute_filepath = os.path.join(recipe_images_directory, filename)
    image = Image.open(absolute_filepath)
    image.save(absolute_filepath, optimize=True)

# TODO: Images could probably be smaller with another library since pillow doesnt seem to have the best optimization
# https://pypi.python.org/pypi/picopt/
# https://pypi.python.org/pypi/pngquant/1.0.5
