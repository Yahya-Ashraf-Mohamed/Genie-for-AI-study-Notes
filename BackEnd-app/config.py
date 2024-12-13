
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import urllib.parse

# Your credentials
username = "moustafatoofii"
password = "QVvp@riy6.2KJ8b" 

# Escaping the username and password
escaped_username = urllib.parse.quote_plus(username)
escaped_password = urllib.parse.quote_plus(password)

# Corrected URI with escaped credentials
# mongodb+srv://moustafatoofii:QVvp@riy6.2KJ8b@sw.rhyx7.mongodb.net/?retryWrites=true&w=majority&appName=sw
uri = f"mongodb+srv://{escaped_username}:{escaped_password}@sw.rhyx7.mongodb.net/?retryWrites=true&w=majority&appName=sw"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))


db = client.genie
test_collection = db["test"]
quiz_collection = db["quiz"]
user_collection = db["user"]
study_material_collection = db["study_material"]
