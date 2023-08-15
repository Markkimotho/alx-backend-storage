#!/usr/bin/env python3
"""Module with an improved version of the Nginx logs"""

from pymongo import MongoClient


def log_stats(mongo_collection):
    """Function that performs the logging on Nginx logs
    Args: mongo_collection - collection object
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

    # Top IPs
    top_ips = mongo_collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])

    print("IPs:")
    for ip in top_ips:
        print(f"\t{ip['_id']}: {ip['count']}")


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx

    log_stats(logs_collection)
