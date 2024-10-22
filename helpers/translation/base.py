import abc


class TranslationInit(abc.ABC):
    @abc.abstractmethod
    def translation_to_object(self, *args, **kwargs):
        raise NotImplementedError
