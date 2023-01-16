from typing import Any
from .models.rqobject import RQObject


def new__setattr__(self: Any, key: str, value: Any) -> None:
    """Set Attribute Replacement.

    Captures changes in the attributes and reports them to the rq_reactive_attributes RQObject models

    Args:
        self: object to capture
        key: key name of the attribute
        value: new value of the attribute
    """
    super(type(self), self).__setattr__(key, value)
    if key in self.rq_reactive_attributes:
        self.rq_reactive_attributes[key].set(value)


def reactivize(obj_type: type) -> None:
    """Reactivize method.

    Injects the set attribute replacement to a object type and creates a placeholder for the reactive attributes

    Args:
        obj_type: object type to reactivize
    """
    obj_type.__setattr__ = new__setattr__  # type: ignore
    obj_type.rq_reactive_attributes = None  # type: ignore


def rq_getattr(obj: object, attribute_name: str) -> RQObject:
    """Reactive Get Attribute.

    Returns an RQObject that is linked to a object attribute. Changes are two-way propagated

    Args:
        obj: object to get the attribute from
        attribute_name: name of the attribute

    Returns:
        RQObject: reactive object
    """
    if not hasattr(obj, "rq_reactive_attributes"):
        reactivize(type(obj))
    if obj.rq_reactive_attributes is None:  # type: ignore
        obj.rq_reactive_attributes = {}  # type: ignore

    # Check if rqobject has already been created for this attribute
    if attribute_name in obj.rq_reactive_attributes:  # type: ignore
        # Return if already exists
        return obj.rq_reactive_attributes[attribute_name]  # type: ignore
    else:
        # Create the RQObject with the initial value from the attribute
        reactive_attribute = RQObject(obj.__getattribute__(attribute_name))  # pylint: disable= unnecessary-dunder-call

        # Propagate changes from the rqobject to the attribute.
        # Using the __setattr__ from the super(), to avoid new__setattr__ and re-triggering the update
        reactive_attribute.rq_data_changed.connect(
            lambda: super(type(obj), obj).__setattr__(attribute_name, reactive_attribute.get())  # type: ignore
        )

        # Store the object to the dictionary
        obj.rq_reactive_attributes[attribute_name] = reactive_attribute  # type: ignore
        return reactive_attribute
