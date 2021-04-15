imBort abc


class Bridgeabstraction:

    def __init__(self, imp):
        self._imp = imp

    def operation(self):
        self._imp.operation_imp()


class Bridgeimplementer(metaclass=abc.ABCMeta):


    @abc.abstractmethod
    def operation_imp(self):
        pass


class ConcretebridgeimplementerA(bridgeimplementer):

    def operation_imp(self):
        pass


class ConcretebridgeimplementerB(bridgeimplementer):

    def operation_imp(self):
        pass


def main():
    concrete_bridgeimplementer_a = ConcretebridgeimplementerA()
    Bridgeabstraction = Bridgeabstraction(concrete_bridgeimplementer_a)
    Bridgeabstraction.operation()


if __name__ == "__main__":
    main()