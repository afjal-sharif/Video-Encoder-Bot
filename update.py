import os
import subprocess
import requests
import logging

if os.path.exists('log.txt'):
    with open('log.txt', 'r+') as f:
        f.truncate(0)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
                    level=logging.INFO)

UPSTREAM_REPO = os.environ.get('UPSTREAM_REPO', None)
try:
    if len(UPSTREAM_REPO) == 0:
       raise TypeError
except TypeError:
    UPSTREAM_REPO = "https://github.com/afjal-sharif/Video-Encoder-Bot"

if os.path.exists('.git'):
    subprocess.run(["rm", "-rf", ".git"])

subprocess.run([f"git init -q \
                  && git config --global user.email bdh@gmail.com \
                  && git config --global user.name bdh \
                  && git add . \
                  && git commit -sm update -q \
                  && git remote add origin {UPSTREAM_REPO} \
                  && git fetch origin -q \
                  && git reset --hard origin/master -q"], shell=True)
