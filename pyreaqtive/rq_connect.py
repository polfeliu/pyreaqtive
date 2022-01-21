from abc import ABC, abstractmethod
from typing import Any, Callable, Optional

from .models import RQModel


class AbstractConversion(ABC):

    @abstractmethod
    def convert_a_to_b(self, a: Any) -> Any:
        raise NotImplemented

    @abstractmethod
    def convert_b_to_a(self, b: Any) -> Any:
        raise NotImplemented


class Conversion(AbstractConversion):

    def __init__(self,
                 a_to_b: Callable[[Any], Any],
                 b_to_a: Callable[[Any], Any]
                 ):
        self.a_to_b = a_to_b
        self.b_to_a = b_to_a

    def convert_a_to_b(self, a: Any) -> Any:
        return self.a_to_b(a)

    def convert_b_to_a(self, b: Any) -> Any:
        return self.b_to_a(b)


class LinearConversion(AbstractConversion):

    def __init__(self, scale_a_to_b: float, offset_a_to_b: Optional[float] = None):
        self.scale_a_to_b = scale_a_to_b
        self.offset_a_to_b = offset_a_to_b

    def convert_a_to_b(self, a: Any) -> Any:
        return a * self.scale_a_to_b + self.offset_a_to_b

    def convert_b_to_a(self, b: Any) -> Any:
        return (b - self.offset_a_to_b) / self.scale_a_to_b


class RQConnect:

    def __init__(
            self,
            model_a: RQModel,
            model_b: RQModel,
            conversion: AbstractConversion
    ):
        self.model_a = model_a
        self.model_b = model_b
        self.conversion = conversion

        self.propagating = False
        self.model_a.rq_data_changed.connect(self._propagate_a_to_b)
        self.model_b.rq_data_changed.connect(self._propagate_b_to_a)
        self._propagate_a_to_b()

    def _propagate_a_to_b(self):
        if not self.propagating:
            print("propagate1")
            self.propagating = True
            self.model_b.set(
                self.conversion.convert_a_to_b(
                    self.model_a.get()
                )
            )
            self.propagating = False

    def _propagate_b_to_a(self):
        if not self.propagating:
            print("propagate2")
            self.propagating = True
            self.model_a.set(
                self.conversion.convert_b_to_a(
                    self.model_b.get()
                )
            )
            self.propagating = False
