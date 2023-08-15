#!/usr/bin/env python3
"""Module for inserting a document in python"""


def insert_school(mongo_collection, **kwargs):
    """Function that performs insertion of a new document
    Args:   mongo_collection - collection to hold document
            kwargs - information to be added(key=value)
    """
    document = mongo_collection.insert_one(kwargs)
    return document.inserted_id
