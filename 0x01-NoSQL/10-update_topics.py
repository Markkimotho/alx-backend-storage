#!/usr/bin/env python3
"""Module that modifies a document's contents"""


def update_topics(mongo_collection, name, topics):
    """Function that changes the topics of a document
    Args:   mongo_collection - collection object
            name - document name to update
            topis - list of topics approached in document
    """
    filter_criteria = {'name': name}
    update_query = {'$set': {'topics': topics}}
    mongo_collection.update_many(filter_criteria, update_query)
