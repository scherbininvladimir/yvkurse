import os
from dotenv import load_dotenv
load_dotenv()

login = os.getenv("LOGIN")
password = os.getenv("PASSWORD")
url = 'https://vk.com/@yvkurse'
output_file = 'output.csv'
