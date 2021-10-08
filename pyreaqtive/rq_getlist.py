from pyreaqtive import RQList


def rq_getlist(obj: object, attribute_name: str) -> RQList:
    l = getattr(obj, attribute_name)
    if isinstance(l, RQList):
        # Already been reactivized
        return l
    elif not isinstance(l, list):
        raise TypeError(f"{attribute_name} of obj is not list")
    else:
        rq_list = RQList(l)
        setattr(obj, attribute_name, rq_list)
        return rq_list
