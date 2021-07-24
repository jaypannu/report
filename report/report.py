import markdown
from jinja2 import Environment, FileSystemLoader
import os

class Report():
    def __init__(self, title=None, name=None, desc=None) -> None:
        self.title = title
        self.name = name
        self.desc = desc
        self.links = ''  # html string 
        self.content = ''  # html string
        self.template = 'base.html'

    def add_title(self, title):
        self.title = title

    def add_name(self, name):
        self.name = name
    
    def add_text(self, text, **kwargs):
        self.content += markdown.markdown(text, **kwargs)

    def add_section(self, section):
        id = section.replace(' ', '')
        self.links += '''<a href="#{}" class="w3-bar-item w3-button">{}</a>\n'''.format(id, section)
        self.content += '''<br><h2 id={}>{}</h2><br>'''.format(id, section)

    def add_table(self, table):
        self.content += table.to_html(classes="w3-table-all")
    
    def add_figure(self, fig):
        self.content += fig.to_html()

    def render(self):
        path = os.path.dirname(os.path.abspath(__file__))
        env = Environment(loader=FileSystemLoader(path))
        template = env.get_template(self.template)
        output_from_parsed_template = template.render(title =self.title, 
                                                       name=self.name, desc=self.desc,
                                                       links=self.links, content=self.content)

        # to save the results
        with open("test.html", "w") as fh:
            fh.write(output_from_parsed_template)


if __name__ == '__main__':
    import logger.logger as logger
    logger.init("starting logger")
    rp = Report()
    logger.info("add section")
    rp.add_section('data frame')
    # create a dummy data frame for testing 
    import pandas as pd
    data = {'Name':['Tom', 'nick', 'krish', 'jack'],
            'Age':[20, 21, 19, 18]}
    df = pd.DataFrame(data)
    rp.add_table(df)
    rp.add_section('Markdown section')
    mk = '''
     Try to put a blank line before...

> This is a blockquote

...and after a blockquote. 
'''
    
    rp.add_text(mk)
    rp.add_section('figure')
    # create dummy plot
    import plotly.express as px
    fig = px.scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16])
    rp.add_figure(fig)
    rp.render()
