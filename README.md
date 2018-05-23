## Channel9 sessions downloader
Easily download session from Microsoft Channel 9 events sessions like //build

# install packages
pip install -r requirements.txt

# configuration
change config.py:

feed_url = 'rss feed url for example: https://s.ch9.ms/Events/Build/2018/RSS/mp4high'
output_dir = 'output folder to store videos, for example: C:\\Users\\gubert\\Videos\\build2018'
filter_keywords = list of keyword to filter, for example: ['vscode','iot','ml','ml.net','dl','deeplearning','machine','learning','ai','device','edge','tensorflow','cognitive','function','functions','train','speech','pyhon','aml','vision','serverless','git','unity','databricks','bot','bots','node.js']

# run
python Channel9SessionsDownloader.py