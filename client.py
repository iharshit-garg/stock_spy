from dotenv import load_dotenv
import os
from massive import RESTClient

load_dotenv()
api_key = os.getenv("API_KEY")
client = RESTClient(api_key=api_key)