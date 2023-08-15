#!/usr/bin/env python3
"""Module that orders students"""


def top_students(mongo_collection):
    """Function that returns all students sorted by average score:
    Args: mongo_collection - collection object
    """
    pipeline = [
        {
            '$project': {
                'name': 1,
                'topics': 1,
                'averageScore': {
                    '$avg': '$topics.score'
                }
            }
        },
        {
            '$sort': {
                'averageScore': -1
            }
        }
    ]
    return list(mongo_collection.aggregate(pipeline))
