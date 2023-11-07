
class DistronodeRunnerException(Exception):
    """ Generic Runner Error """


class ConfigurationError(DistronodeRunnerException):
    """ Misconfiguration of Runner """


class CallbackError(DistronodeRunnerException):
    """ Exception occurred in Callback """
