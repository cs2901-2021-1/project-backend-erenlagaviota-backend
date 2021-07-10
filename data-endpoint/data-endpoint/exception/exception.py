class PeriodRangeError(Exception):
    """Exception raised for errors in the period range.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Error ocurred while filtering by period range"):
        self.message = message
        super().__init__(self.message)


class PeriodError(Exception):
    """Exception raised for errors in the period.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Error ocurred while filtering periods"):
        self.message = message
        super().__init__(self.message)