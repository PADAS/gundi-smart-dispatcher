

class ConfigurationNotFound(Exception):
    pass


class ConfigurationValidationError(Exception):
    pass


class ReferenceDataError(Exception):
    pass


class DispatcherException(Exception):
    pass


class TooManyRequests(DispatcherException):
    pass
