from .models.rqobject import RQObject


def new__setattr__(self, key, value):
    super(type(self), self).__setattr__(key, value)
    if hasattr(self, "rq_reactive_attributes"):
        if self.rq_reactive_attributes is not None:
            if key in self.rq_reactive_attributes:
                self.rq_reactive_attributes[key].set(value)


def reactivize(obj_type):
    obj_type.__setattr__ = new__setattr__
    obj_type.rq_reactive_attributes = None


def rq_getattr(obj: object, attribute_name):
    if not hasattr(obj, "rq_reactive_attributes"):
        reactivize(type(obj))
    if obj.rq_reactive_attributes is None:
        obj.rq_reactive_attributes = {}
    reactive_attribute = RQObject(obj.__getattribute__(attribute_name))
    reactive_attribute.rq_data_changed.connect(
        lambda: super(type(obj), obj).__setattr__(attribute_name, reactive_attribute.get())
    )
    obj.rq_reactive_attributes[attribute_name] = reactive_attribute
    return reactive_attribute
