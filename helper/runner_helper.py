from abc import ABCMeta, abstractmethod

from helper.storage_helper import Exhibition, JustJsonStorage


class RunnerInit(metaclass=ABCMeta):
    storage = None
    target_storage = None
    target_systematics = None
    use_storage = JustJsonStorage
    exhibition_model = Exhibition

    def init_storage(self, need_init=True):
        if hasattr(self, "use_storage") and need_init:
            self.storage = self.use_storage(
                self.target_storage, self.target_systematics
            )
            self.storage.truncate_table()

    def write_storage(self, data):
        if self.storage is not None:
            self.storage.create_data(data)

    def commit_storage(self):
        if self.storage is not None:
            self.storage.commit()

    @abstractmethod
    def get_response(self, *args, **kwargs) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_items(self, *args, **kwargs) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_parsed(self, *args, **kwargs):
        raise NotImplementedError

    def run(self):
        self.init_storage()
        response = self.get_response()
        items = self.get_items(response)
        exhibitions = self.get_parsed(items)
        for exhibition in exhibitions:
            self.write_storage(exhibition.dict())
        self.commit_storage()
