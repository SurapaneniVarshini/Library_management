import os
import json
from pymongo import MongoClient
from bson import ObjectId, json_util  # Add this import for custom JSON encoder

MONGO_CONNECTION_STRING = "mongodb+srv://varshinisurapaneni0211:varshini1234@clusterlibrary.1vvke4p.mongodb.net/library_management_system"
DB_NAME = "library_management_system"
OUTPUT_FOLDER = "./output"  # Replace this with the desired output folder path

# Custom JSON encoder to handle BSON data
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

def download_mongodb_database(connection_string, db_name, output_folder):
    # Connect to MongoDB
    client = MongoClient(connection_string)

    # Get the specified database
    db = client[db_name]

    # Fetch the data from the collections in the database
    data = {}
    for collection_name in db.list_collection_names():
        collection_data = list(db[collection_name].find())
        data[collection_name] = collection_data

    # Save the data to a JSON file using the custom JSON encoder
    output_file = os.path.join(output_folder, f"{db_name}.json")
    with open(output_file, "w") as file:
        json.dump(data, file, indent=4, default=json_util.default, cls=CustomJSONEncoder)

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    download_mongodb_database(MONGO_CONNECTION_STRING, DB_NAME, OUTPUT_FOLDER)
    print("Database download completed!")
