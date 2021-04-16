from __future__ import annotations
from abc import ABC, abstractmethod, abstractproperty
from typing import Any
import covidify.data_visualization as visualization

class ReportBuilder(ABC):

    @abstractproperty
    def report(self) -> None:
        pass

    @abstractmethod
    def produce_graph(self) -> None:
        pass

    @abstractmethod
    def produce_table(self) -> None:
        pass

class ConcreteReportBuilder(ReportBuilder):

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self._report = Report1()

    @property
    def report(self) -> Report1:
        report = self._report
        self.reset()
        return report

    def produce_graph(self) -> None:
        print("Creating Graph...")
        self._report.add(visualization.create_graph())

    def produce_table(self) -> None:
        print("Creating Table...")
        self._report.add(visualization.create_table())

class Report1():

    def __init__(self) -> None:
        self.parts = []

    def add(self, part: Any) -> None:
        self.parts.append(part)

    def list_parts(self) -> None:
        print(f"Test Output: {', '.join(self.parts)}", end="")

class Director:

    def __init__(self) -> None:
        self._builder = None

    @property
    def builder(self) -> ReportBuilder:
        return self._builder

    @builder.setter
    def builder(self, builder: ReportBuilder) -> None:
        self._builder = builder

    def build_graph(self) -> None:
        self.builder.produce_graph()

    def build_table(self) -> None:
        self.builder.produce_table()

    def build_table_garph(self) -> None:
        self.builder.produce_table()
        self.builder.produce_graph()