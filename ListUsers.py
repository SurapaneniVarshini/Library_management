from pymongo import MongoClient

# MongoDB connection settings
MONGO_HOST = "localhost"
MONGO_PORT = 27017
DB_NAME = "library_management_system"
COLLECTION_NAME = "users"

def retrieve_all_users():
    try:
        # Establish a connection to MongoDB
        client = MongoClient(MONGO_HOST, MONGO_PORT)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        # Retrieve all documents from the collection
        all_users = collection.find()

        # Print the information of each user
        for user in all_users:
            print("User ID:", user.get("id"))
            print("Username:", user.get("username"))
            print("Password:", user.get("password"))
            print("Full Name:", user.get("full_name"))
            print("Address:", user.get("address"))
            print("Phone Number:", user.get("phone_number"))
            print("Email:", user.get("email"))
            print("Role:", user.get("role"))
            print("=" * 30)

    except Exception as e:
        print("An error occurred:", str(e))

    finally:
        client.close()

if __name__ == "__main__":
    retrieve_all_users()
