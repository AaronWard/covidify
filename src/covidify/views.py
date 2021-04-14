from abc import ABCMeta, abstractstaticmethod

#Bridge Pattern connected to iDataResource
#Abstract View class

class View(metaclass=ABCMeta):

    dataResource = iDataResource()

    #Constructor needs an iDataResource r
    def __init__(self,  r):
        self.dataResource = r

    
    @abstractstaticmethod
    def display():
        "Displays data resourse visualization in different types ofviews"


    
#Concrete Classes of Abstraction class View

#Creates concrete View that shows any and all data from resource type -- formated windows and sections show details and forcasts
class CompleteView(View):   

    def display(self):
     self.dataResource.graph()
     #displays graph that is created by the concrete resource class

#Creates a concrete View that shows extended details and extra data from concrete resource type used -- formated windows are larger
class ExtendedView(View):   

    def display(self):
     self.dataResource.createGraph()
     #displays graph that is created by the concrete resource class

#Creates a concrete View that shows simple and quick  data from concrete resource used -- formated windows are small with no graphics
class QuickView(View):   

    def display(self):
     self.dataResource.createGraph()
     #displays graph that is created by the concrete resource class
     
