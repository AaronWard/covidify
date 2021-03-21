

class Data:
    def __init__(self, value):
        self.__value = value

    def get_value(self):
        return self.__value

    def set_value(self, new_Value):
        self.__value = new_Value

class Figure:
    def __init__(self, fig, title):
        self.__title = title
        self.__figure = fig
    
    def get_title(self):
        return self.__title

    def get_figure(self):
        return self.__figure

class Coloumn:
    def __init__(self, title):
        self.__title = title
        self.__data = []

    def set_new_data(self, value):
        self.__data.append(Data(value))

    def set_title(self, title):
        self.__title = title

    def get_title(self):
        return self.__title

    def get_data(self):
        return self.__data

class Sheet():
    def __init__(self, title):
        self.__title = title
        self.__coloumns = []
        self.__figures = None

    def set_new_coloumn(self, title):
        self.__coloumns.append(Coloumn(title))

    def set_new_figure(self, title, fig):
        self.__figures.append(Figure(fig, title))

    def set_title(self, title):
        self.__title = title

    def get_title(self):
        return self.__title

    def get_coloumns(self):
        return self.__coloumns

    def get_figures(self):
        return self.__figures
        

class Report:
    def __init__(self, title):
        self.__title = title
        self.__sheets = []

    def set_new_sheet(self, title):
        self.__sheets.append(Sheet(title))

    def set_title(self, title):
        self.__title = title

    def get_title(self):
        return self.__title

    def get_sheets(self):
        return self.__sheets