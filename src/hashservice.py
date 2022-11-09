# interface p/ hash_service
from abc import ABC, abstractmethod


class HashService(ABC):

    @abstractmethod
    def hash(self, pwd):
        raise (NotImplementedError)

    @abstractmethod
    def check(self, pwd, hashed):
        raise (NotImplementedError)
