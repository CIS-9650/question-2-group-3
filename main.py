# importing all the libraries that are required for the script
import requests
import json
import pandas as pd
import numpy as np
import re
from urllib.parse import quote
from bs4 import BeautifulSoup
import time
import sqlite3
import certifi
import ssl

# Create a custom SSL context using certifi's CA bundle
ssl_context = ssl.create_default_context(cafile=certifi.where())
ssl._create_default_https_context = lambda: ssl_context  


