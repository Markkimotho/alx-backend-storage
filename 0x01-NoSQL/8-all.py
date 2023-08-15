#!/usr/bin/env python3
"""Module that lists all documents in a collection"""
import pymongo


def list_all(mongo_collection):
    """Function that lists the documents in the collection
    Args: mongo_collection - The collection with the documents
    """
    document_list = []

    documents = mongo_collection.find()
    for document in documents:
        document_list.append(document)
    return document_list
