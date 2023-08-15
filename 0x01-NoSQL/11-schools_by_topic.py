#!/usr/bin/env python3
"""Module that returns documents based on the topic"""


def schools_by_topic(mongo_collection, topic):
    """Function that returns the list of school having a specific topic
    Args:   mongo_collection - collection object
            topic - topic to be searched
    """
    filter_criteria = {'topics': topic}
    schools = mongo_collection.find(filter_criteria)
    return list(schools)
