"""Module exceptions."""
__author__ = 'Joan A. Pinol  (japinol)'

class LoadGameException(Exception):
    pass


class LoadGameNoSavedGameDataException(LoadGameException):
    pass


class LoadGameWrongVersionException(Exception):
    pass


class LoadGamePcException(LoadGameException):
    pass


class LoadGameNPCsException(LoadGameException):
    pass


class LoadGameItemsException(LoadGameException):
    pass


class SaveGameException(Exception):
    pass


class SaveGamePcException(SaveGameException):
    pass


class SaveGameNPCsException(SaveGameException):
    pass


class SaveGameItemsException(SaveGameException):
    pass
