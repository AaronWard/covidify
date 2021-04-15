from __future__ import annotations
from abc import ABC, abstractmethod


class ChartView:
    #abstraction

    def __init__(self, InterfaceResource: InterfaceResource) -> None:
        self.InterfaceResource = InterfaceResource

    def operation(self) -> str:
        return (f"ChartView: Base operation with:\n"
                f"{self.InterfaceResource.operation_InterfaceResource()}")


class LineChart(ChartView):
    #concrete abstraction

    def operation(self) -> str:
        return (f"LineChart: Extended operation with:\n"
                f"{self.InterfaceResource.operation_InterfaceResource()}")


class InterfaceResource(ABC):
    #implementation

    @abstractmethod
    def operation_InterfaceResource(self) -> str:
        pass


#concrete implementation
class DataFeedResourceA(InterfaceResource):
    def operation_InterfaceResource(self) -> str:
        return "DataFeedResourceA: Here's the result on the platform A."


class DataFeedResourceB(InterfaceResource):
    def operation_InterfaceResource(self) -> str:
        return "DataFeedResourceB: Here's the result on the platform B."


def client_side(ChartView: ChartView) -> None:


    print(ChartView.operation(), end="")



if __name__ == "__main__":


    InterfaceResource = DataFeedResourceA()
    ChartView = ChartView(InterfaceResource)
    client_side(ChartView)

    print("\n")

    InterfaceResource = DataFeedResourceB()
    ChartView = LineChart(InterfaceResource)
    client_side(ChartView)