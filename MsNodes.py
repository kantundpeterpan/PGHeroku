import ipytree as it
import pandas as pd
import os
from traitlets import Unicode

class FolderNode(it.Node):
    def __init__(self, *args, **kwargs):
        super(FolderNode, self).__init__(*args, **kwargs)

class DataNode(it.Node):
    file = Unicode()
    def __init__(self, *args, **kwargs):
        self.file = kwargs.pop('file')
        self.parent = kwargs.pop('parent')
        super(DataNode, self).__init__(*args, **kwargs)
        self.observe(self.selected_handle, 'selected')
    
    def selected_handle(self, event):
        global l
        global p
        df = pd.read_csv(self.file)

        l.data_source.data['x'] = df.x
        l.data_source.data['y'] = df.y
        
        p.title.text = ' '.join([self.parent.name, self.name])

class DataTree(it.Tree):
    
    @classmethod
    def from_path(cls, path='./'):
        folders = []
        for root, dirs, files in os.walk('./'):
            dirs = [d for d in dirs if not d.startswith('.') and not d.startswith('_')]
            dirs.sort()
            for d in dirs:
                n = FolderNode(d)
                for f in os.listdir(d):
                    dn = DataNode(os.path.splitext(f)[0], 
                                  file = os.path.join('./', d, f),
                                  parent = n)
                    #dn.observe(dn.file_on_event, 'selected')
                    n.add_node(dn)
                folders.append(n)
        
        return cls(folders)
    
from bokeh.plotting import figure, output_file, show
from bokeh.themes import built_in_themes
from bokeh.io import curdoc

# prepare some data
x = [0]
y = [0]

# create a new plot with a title and axis labels
p = figure(title="simple line example", x_axis_label='x', y_axis_label='y',
           width=1000, height=400)

# add a line renderer with legend and line thickness
l = p.line(x, y, line_width=2)

curdoc().theme = 'dark_minimal'
