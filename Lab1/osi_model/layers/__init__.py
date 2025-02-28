from abc import ABC, abstractmethod

class Layer(ABC):
    """Base abstract class for all OSI layers"""
    
    def __init__(self, name):
        self.name = name
    
    @abstractmethod
    def send_down(self, data, **kwargs):
        """Process data and send it down to the layer below"""
        pass
    
    @abstractmethod
    def send_up(self, data, **kwargs):
        """Process data and send it up to the layer above"""
        pass