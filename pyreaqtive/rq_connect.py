from abc import ABC, abstractmethod
from typing import Any, Callable

from .models import RQModel


class AbstractConversion(ABC):
    """Base model for bidirectional conversion of two models."""

    @abstractmethod
    def convert_a_to_b(self, a: Any) -> Any:  # pylint: disable= invalid-name
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def convert_b_to_a(self, b: Any) -> Any:  # pylint: disable= invalid-name
        raise NotImplementedError  # pragma: no cover


class Conversion(AbstractConversion):
    """Conversion Declared with two functions."""

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
    """Linear Conversion Declared with scale and offset."""

    def __init__(self, scale_a_to_b: float, offset_a_to_b: float = 0):
        self.scale_a_to_b = scale_a_to_b
        self.offset_a_to_b = offset_a_to_b

    def convert_a_to_b(self, a: Any) -> Any:
        return a * self.scale_a_to_b + self.offset_a_to_b

    def convert_b_to_a(self, b: Any) -> Any:
        return (b - self.offset_a_to_b) / self.scale_a_to_b


class RQConnect:
    """Bidirectional connection between two models."""

    Conversion = Conversion
    LinearConversion = LinearConversion

    def __init__(
            self,
            model_a: RQModel,
            model_b: RQModel,
            conversion: AbstractConversion
    ):
        self.model_a = model_a
        self.model_b = model_b
        self.conversion = conversion

        self._propagating = False
        self.model_a.rq_data_changed.connect(self._propagate_a_to_b)
        self.model_b.rq_data_changed.connect(self._propagate_b_to_a)
        self._propagate_a_to_b()

    def _propagate_a_to_b(self) -> None:
        if not self._propagating:
            self._propagating = True
            self.model_b.set(
                self.conversion.convert_a_to_b(
                    self.model_a.get()
                )
            )
            self._propagating = False

    def _propagate_b_to_a(self) -> None:
        if not self._propagating:
            self._propagating = True
            self.model_a.set(
                self.conversion.convert_b_to_a(
                    self.model_b.get()
                )
            )
            self._propagating = False
