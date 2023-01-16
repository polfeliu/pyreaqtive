from pyreaqtive import RQList


def rq_getlist(obj: object, attribute_name: str) -> RQList:
    """Reactive Get List.

    Replaces a list of an object by an RQList and returns it

    Warnings:
        This method replaces the list with an RQList, all methods of which are compatible
        with built-in lists. However, the signature of the object is changed from list to RQList.
        Using this method on objects that rely on isinstance or issubclass on the list, will break.

    Args:
        obj: object to the list
        attribute_name: attribute of the object that is the list

    Returns:
        RQList: reactive list object
    """
    lst = getattr(obj, attribute_name)
    if isinstance(lst, RQList):
        # Already been reactivized
        return lst
    elif not isinstance(lst, list):
        raise TypeError(f"{attribute_name} of obj is not a list")
    else:
        rq_list = RQList(lst)
        setattr(obj, attribute_name, rq_list)
        return rq_list
