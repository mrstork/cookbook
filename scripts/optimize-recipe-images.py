import os
import pngquant

CRON_DAILY_DIR = os.path.dirname(os.path.abspath(__file__))
CRON_DIR = os.path.dirname(CRON_DAILY_DIR)
OPENSHIFT_DIR = os.path.dirname(CRON_DIR)
REPO_DIR = os.path.dirname(OPENSHIFT_DIR)

if os.environ.get('OPENSHIFT_APP_DNS'):
    recipe_images_directory = os.path.join(REPO_DIR, 'wsgi', 'static', 'media','recipe-images')
else:
    recipe_images_directory = os.path.join(REPO_DIR, 'wsgi', 'media','recipe-images')

for filename in os.listdir(recipe_images_directory):
    absolute_filepath = os.path.join(recipe_images_directory, filename)
    pngquant.config(absolute_filepath)
    pngquant.quant_image(absolute_filepath)
