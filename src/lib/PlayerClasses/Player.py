from abc  import ABC, abstractmethod
from copy import deepcopy

class Player(ABC):
    @abstractmethod
    def take_turn(self):
        pass

    