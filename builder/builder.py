class Plotter(ABC):

    @abstractmethod
    def setTitle(self):
        pass

    @abstractmethod
    def setXlabel(self):
        pass

    @abstractmethod
    def setYlabel(self):
        pass

    @abstractmethod
    def getResult(self):
        pass


class Graph():
    def __init__(self):
        self.Xcol = None
        self.Ycol = None
        self.style = None
        self.title = None
        self.Xlabel = None
        self.Ylabel = None
        self.grid = None

    
class ScatterPlotterv1(Plotter):
    def __init__(self):
        self.graph = Graph()
        self.x = 10
        self.y = 6
        self.style = 'o'

    def setXlabel(self, xl):
        self.graph.Xlabel = xl
        return self.graph

    def setYlabel(self, yl):
        self.graph.Ylabel = yl
        return self.graph 

    def setTitle(self, t):
        self.graph.title = t
        return self.graph

    def getResult(self):
        return self.graph


class ScatterPlotterv2(Plotter):
    def __init__(self):
        self.graph = Graph()
        self.style = 'o'

    def setXcol(self, x):
        self.graph.Xcol = x
        return self.graph

    def setYcol(self, y):
        self.graph.Ycol = y
        return self.graph

    def setStyle(self, s):
        self.graph.style = s
        return self.graph

    def setTitle(self, t):
        self.graph.title = t
        return self.graph

    def setXlabel(self, xl):
        self.graph.Xlabel = xl
        return self.graph

    def setYlabel(self, yl):
        self.graph.Ylabel = yl
        return self.graph 

    def getResult(self):
        return self.graph


class SeriesPlotter(Plotter):
    def __init__(self):
        self.graph = Graph()
        self.start = 0
        self.end = None
        self.format = '-'

    def setTime(self):
        self.time = time[start, end]
        return self.graph

    def setXlabel(self, xl):
        self.graph.setXlabel = xl
        return self.graph

    def setYlabel(self, yl):
        self.graph.setYlabel = yl
        return self.graph

    def setGrid(self, g):
        self.graph.grid = g
        return self.graph

    def getResult(self):
        return self.graph

    
class Director:
    def __init__(self) -> None:
        self._builder = None

    def setGraph(self, graph):
        self.graph = graph
