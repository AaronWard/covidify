from abc import ABCMeta, abstractstaticmethod

#Bridge Pattern Connected to Views
#Abstract Data Resource Class

class iDataResource(metaclass=ABCMeta):
   
    @abstractstaticmethod
    def graph():
        pass

    @abstractstaticmethod
    def snippet():
        pass
    @abstractstaticmethod
    def getcreateGraph():
        pass



# Concrete Classes of iDataResource


#concrete class of IDataResource that creates a Pie Graph using builder class
class PieGraph(iDataResource):   
    
    resource = Director.construct_Vis()
    
    #grabs graph from builder that injects params to data_visualiazation to create graph
    def graph(self):
        self.resource.getcreateGraph()

    #Grabs covid numbers and quickly gets formated string to display quickly
    def quickLook(self):
        self.resource.getDataCount().toFormatedString()
    
    

#concrete class of IDataResource that creates a Bar Graph using builder class
class BarGraph(iDataResource):   

    resource = Director.construct_Vis()
    
    #grabs graph from builder that injects params to data_visualiazation to create graph
    def graph(self):
         self.resource.getcreateGraph()

    #Grabs covid numbers and quickly gets formated string to display quickly
    def quickLook(self):
        self.resource.getDataCount().toFormatedString()
    
    


#concrete class of IDataResource that creates a Forcast Graph - in some format using builder class
class ForcastGraph(iDataResource):   

    resource = Director.construct_Vis()

    #Grabs Graph from builder that injects params to data_visualiazation to create graph
    def graph(self):
         self.resource.getcreateGraph()

    #Grabs covid numbers and quickly gets formated string to display quickly
    def quickLook(self):
        self.resource.getDataCount().toFormatedString()
    
    

     
