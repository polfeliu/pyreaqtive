from .rqmodel import RQModel, RQComputedModel


class RQText(RQModel):
    """Reactive Text Model

    Represents a string of text
    """

    def __init__(self, text: str):
        """Constructor

        Args:
            text: Initial value of the model
        """
        super(RQText, self).__init__()
        self._text: str = text
        """Model store variable"""

    def get(self) -> str:
        """Get value of the model

        Returns:
            str: value of the model
        """
        return self._text

    def set(self, value: str) -> None:
        """Will propagate the change to the widgets linked to the model

        Args:
            value: new value of the model
        """
        self._text = value
        self.rq_data_changed.emit()

    def __str__(self) -> str:
        """Get value of the model in string format

        Returns:
            str: value of the model
        """
        return self.get()


class RQComputedText(RQComputedModel, RQText):
    """Reactive Computed Float Model"""

    def __init__(self, format_string: str, **kwargs):
        """Constructor

        Args:
            format_string: python formatting string

            **kwargs: reactive models in the function by variable name as keyword
                Changes in these models will trigger recalculation of the function
       """
        self.rq_format_string = format_string
        RQComputedModel.__init__(self, self._format_text, **kwargs)
        RQText.__init__(self, self.get())

    def _format_text(self, **kwargs) -> str:
        """Get value of the model in string format

        Args:
            **kwargs: arguments to inject in the string

        Returns:
            str: formatted string with current model values
        """
        return self.rq_format_string.format(
            **{key: str(variable) for key, variable in kwargs.items()}
        )

    def get(self) -> str:
        """Get the computed text"""
        return str(super().get())
