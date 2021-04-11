from abc import ABCMeta, abstractstaticmethod

class iBuilder(metaclass=ABCMeta):
    "the Builder Interface"

    @staticmethod
    @abstractstaticmethod
    def build_part_create_trend_line():
        "build Part create_trend_line"

    @staticmethod
    @abstractstaticmethod
    def build_part_create_bar():
        "build Part create_bar"


    @staticmethod
    @abstractstaticmethod
    def build_part_create_stacked_bar():
        "build Part create_stacked_bar"

 

class VisualBuilder(iBuilder):
    "The concrete builder"
    
    def __init__(self):
        self.dataVis = DataVisualization()

    #Builder Part for create_trend_line
    def build_part_create_trend_line(self):
        self.dataVis.paramParts.append('tmp_df, date_col, col, col2, col3, fig_title, country')
        return self
    
    #Builder Part for create_bar
    def build_part_create_bar(self):
        self.dataVis.paramParts.append('tmp_df, col, rgb, country')
        return self
    
    #Builder Part for stacked_bar
    def build_part_create_stacked_bar(self):
        self.dataVis.paramParts.append('tmp_df, col1, col2, fig_title, country')
        return self

    def get_result_params(self):
        return self.dataVis


class DataVisualization():
    "The Data Visualizer Params"

    def __init__(self):
        self.paramParts = []
        




class Director:
    "The Director, using chosen params builds complex data visualization"  

    @staticmethod
    def construct_Vis():
        "constructs the methods with chosen params"
        return VisualBuilder()\
                .build_part_create_trend_line()\
                    .build_part_create_bar()\
                        .build_part_create_stacked_bar()\
                            .get_result_params()




#Client Use Example
PARAMS = Director.construct_Vis()
print(PARAMS.paramParts)
#prints and shows the params to build visualization parts

#Index 0 - contains parameters to build create_trend_line
#Index 1 - contains parameters to build crreate_bar
#Index 2 - contains parameters to build create_stacked_bar
#print(PARAMS.paramParts[0]) 
#print(PARAMS.paramParts[1]) 
#print(PARAMS.paramParts[2]) 


#Class/Method in which builder will be used for
"""def create_trend_line(tmp_df, date_col, col, col2, col3, fig_title, country):
    fig, ax = plt.subplots(figsize=(20,10))
    tmp_df.groupby([date_col])[[col, col2, col3]].sum().plot(ax=ax, marker='o')
    ax.set_title(create_title(fig_title, country))
    fig = ax.get_figure()
    fig.savefig(os.path.join(image_dir, create_save_file(col, country, 'trendline')))

def create_bar(tmp_df, col, rgb, country):
    tmp_df = tmp_df.tail(120)
    fig, ax = plt.subplots(figsize=(20,10))
    tmp = tmp_df.groupby(['date'])[[col]].sum()
    ax.set_title(create_title(col, country))
    tmp.plot.bar(ax=ax, rot=90, color=rgb)
    fig = ax.get_figure()
    fig.savefig(os.path.join(image_dir, create_save_file(col, country, 'bar')))

def create_stacked_bar(tmp_df, col1, col2, fig_title, country):
    tmp_df = tmp_df.tail(120)
    tmp_df = tmp_df.set_index('date')
    fig, ax = plt.subplots(figsize=(20,10))
    ax.set_title(create_title(fig_title, country))
    tmp_df[[col2, col1]].plot.bar(ax=ax,
                                  rot=90,
                                  stacked=True)
    fig = ax.get_figure()
    fig.savefig(os.path.join(image_dir, create_save_file(col2, country, 'stacked_bar')))"""



