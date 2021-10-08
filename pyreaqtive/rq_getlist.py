from typing import List

from pyreaqtive import RQList


def rq_getlist(obj: object, attribute_name: str):
    # TODO Cache, check that is a list
    rq_list = RQList(getattr(obj, attribute_name))
    setattr(obj, attribute_name, rq_list)
    return rq_list
