import os

# * This file is only imported in dev or pro enviroment mode
# * So tests are runned with memory event store

os.environ["INFRASTRUCTURE_FACTORY"] = "eventsourcing.sqlite:Factory"
os.environ["SQLITE_DBNAME"] = "event_store.db"
