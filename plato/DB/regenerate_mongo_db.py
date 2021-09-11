import os
import pymongo

from dotenv import load_dotenv
load_dotenv()


def main():
    if os.environ["ENV_MODE"] == "Test":
        mongo_client = pymongo.MongoClient(os.environ["MONGODB_URL"])
        mongo_client.drop_database(os.environ["MONGODB_DBNAME"])


if __name__ == "__main__":
    main()
