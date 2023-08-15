#!/usr/bin/env python3
"""Module for providing nginx log stats stored in mongoDB"""
from pymongo import MongoClient


def log_stats(mongo_collection):
    """Function that provides log stats for Nginx
    Args: mongo_collection - object that stores the logs
    """
    # Total number of logs
    total_logs = mongo_collection.count_documents({})

    print(f"{total_logs} logs")

    # Methods
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        count = mongo_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    # Status check
    status_check = mongo_collection.count_documents(
            {"method": "GET", "path": "/status"})
    print(f"{status_check} status check")


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx

    log_stats(logs_collection)
