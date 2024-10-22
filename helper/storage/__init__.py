import abc


class StorageInit(abc.ABC):

    @staticmethod
    def login(*args, **kwargs):
        raise NotImplementedError

    @staticmethod
    def upload(*args, **kwargs):
        raise NotImplementedError
