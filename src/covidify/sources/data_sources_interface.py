import abc

class DataInterface(object, metaclass=abc.ABCMeta):

    def __init__(self):
        pass

    @abc.abstractmethod
    def get():
        raise NotImplementedError('User must define get()')
