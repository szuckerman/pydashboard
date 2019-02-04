from dominate.tags import *
from dominate.util import raw, text
from flask import Flask, render_template
from jinja2 import Environment, FileSystemLoader

import tempfile
import webbrowser


env = Environment(loader=FileSystemLoader('/Users/zucks/PycharmProjects/pydashboard/pydashboard/templates'))


GLOBAL_JS_CODE = []
GLOBAL_DIMENSION_CODE = []


def hello_world(x):
    return "hello %s!" % x


# class Row:
#     def __init__(self, *args):
#         self.children = args
#         # if type(classes) == str:
#         #     self.classname = classes
#         # else:
#         #     self.classname = " ".join("row-" + item for item in classes)
#         self.tags = {"class": "row"}
#         # self.children = children if children else []
#         self.html = div(**self.tags)
#         self._add_child_elements()
#
#     def __repr__(self):
#         return "<Row: {num_children} children>".format(num_children=len(self.children))
#
#     def __str__(self):
#         return str(self.html)
#
#     def _add_child_elements(self):
#         if self.children:
#             for child in self.children:
#                 self.html.add(child.html)
#
#     def __gt__(self, other):
#         self.children.append(other.html)
#         self.html.add(other.html)
#         return self
#
#     def __iadd__(self, other):
#         self.children.append(other.html)
#         self.html.add(other.html)
#         return self


# class Col:
#     def __init__(self, children=None, classes=None, name=None):
#         self.classes = classes
#         self.classname = " ".join("col-" + item for item in classes)
#         self.tags = {"class": self.classname}
#         self.children = self._instantiate_children(children)
#         self.html = div(**self.tags)
#         self._add_child_elements()
#
#     def _instantiate_children(self, children):
#         if type(children) == list:
#             return children
#         elif len(children) > 0:
#             return [children]
#         else:
#             return []
#
#     def __repr__(self):
#         return "<{cls}: {classname}, {num_children} children>".format(
#             cls=__class__.__name__,
#             classname=self.classname,
#             num_children=len(self.children),
#         )
#
#     def __str__(self):
#         return str(self.html)
#
#     def _add_child_elements(self):
#         if self.children:
#             for child in self.children:
#                 if type(child) == str:
#                     self.html.add(raw(child))
#                 else:
#                     self.html.add(child.html)
#                 if hasattr(child, "js_chart_code"):
#                     GLOBAL_JS_CODE.append(child.js_chart_code)
#
#     def __gt__(self, other):
#         self.children.append(other.html)
#         self.html.add(other.html)
#         return self
#
#     def __lt__(self, other):
#         self.children.append(other.html)
#         self.html.add(other.html)
#         return self
#
#     def __iadd__(self, other):
#         self.children.append(other.html)
#         self.html.add(other.html)
#         return self
#
#     def __getitem__(self, index):
#         return self.children[index]


# class ChartElement:
#     def __init__(self, name=None, height=None, cls=None, id=None):
#         self.name = name
#         self.id = id
#         self.height = height
#         self.cls = cls
#         self.tags = {"id": self.name}
#         if height:
#             self.tags["style"] = "height: {height}vh".format(height=self.height)
#         if cls:
#             self.tags["class"] = self.cls
#         self.html = div(self.name, **self.tags)
#
#     def __str__(self):
#         return str(self.html)
#
#     def __len__(self):
#         return 1

# IMMEDIATE PREVIOUS VERSION
# class ChartElement(div):
#     def __init__(self, height=None, id=None, *args, **kwargs):
#         super().__init__(id=id, *args, **kwargs)
#         # self.id = id
#         self.height = height
#         # self.tags = {"id": self.id}
#         self.__class__.__name__ = 'div'
#         if self.height:
#             self.update_height(self.height)
#
#     def update_height(self, height):
#         self.height = height
#         self.set_attribute('style',
#                            'height: {height:.0f}vh'.format(height=(100 - self.padding * 2) * self.height / 100))
#


class ChartElement(div):
    def __init__(self, id=None, height=None, padding=5, *args, **kwargs):
        super().__init__(id=id, *args, **kwargs)
        self.id=id
        self.height=height
        self.padding=padding
        self.__class__.__name__ = 'div'
        self.add(text(self.id))
        if self.height:
            self.update_height(self.height)

    def update_height(self, height):
        self.height = height
        self.set_attribute('style', 'height: {height:.0f}vh'.format(height=(100 - self.padding * 2) * self.height / 100))


# item = ChartElement(id="something", height=100)

class Dashboard:
    def __init__(self, *items, data=None, template=None):
        self.data = data
        self.items = items
        self.template = template
        self.html = div(self.item_str, {"class": "container"})
        self.outline_html = None
        GLOBAL_JS_CODE = [str(item) for item in self.items]
        self.my_string = "\n".join(GLOBAL_JS_CODE)

    def add_template(self, *items):
        item_str = [raw(str(item)) for item in items]
        self.outline_html = div(item_str, {"class": "container"})

    @property
    def item_str(self):
        return [raw(str(item)) for item in self.items]

    def show_chart_outlines(self):
        return str(self.html)

    def view_outlines(self):

        template = env.get_template('dashboard_outline.html')

        html_output = template.render(dashboard_outline=self.template)

        tmp = tempfile.NamedTemporaryFile(delete=False)
        path = tmp.name + '.html'
        f = open(path, 'w')
        f.write(html_output)
        f.close()
        webbrowser.open('file://' + path)

    def run(self, host="127.0.0.1", port=5000, debug=False):
        app = Flask(__name__)

        @app.route("/")
        def index():
            return render_template(
                "dashboard.html",
                dimensions="\n".join(GLOBAL_DIMENSION_CODE),
                json_dat=self.data.to_json(orient="records"),
                chart_code=self.my_string,
                dashboard=self.template
            )

        app.run(host=host, port=port, debug=debug)

    def view(self):
        template = env.get_template('dashboard.html')

        html_output = template.render(
            dimensions="\n".join(GLOBAL_DIMENSION_CODE),
            json_dat=self.data.to_json(orient="records"),
            chart_code=self.my_string,
            dashboard=self.template
        )

        tmp = tempfile.NamedTemporaryFile(delete=False)
        path = tmp.name + '.html'
        f = open(path, 'w')
        f.write(html_output)
        f.close()
        webbrowser.open('file://' + path)


class Row(div):
    def __init__(self, other=None, height=None, padding=5, *args, **kwargs):
        super().__init__(cls='row', *args, **kwargs)
        self.height=height
        self.padding=padding
        self.__class__.__name__ = 'div'
        if self.height:
            self.update_height(self.height)
        if other:
            if not isinstance(other, list):
                self.add(other)
            else:
                for element in other:
                    self.add(element)

    def update_height(self, height):
        self.height = height
        self.set_attribute('style', 'height: {height:.0f}vh'.format(height=(100 - self.padding * 2) * self.height / 100))


class Container(div):
    def __init__(self, other=None, height=None, padding=5, *args, **kwargs):
        super().__init__(cls='container', *args, **kwargs)
        self.height=height
        self.padding=padding
        self.__class__.__name__ = 'div'
        if self.height:
            self.update_height(self.height)
        if other:
            if not isinstance(other, list):
                self.add(other)
            else:
                for element in other:
                    self.add(element)

    def update_height(self, height):
        self.height = height
        self.set_attribute('style', 'height: {height:.0f}vh'.format(height=(100 - self.padding * 2) * self.height / 100))



class Col(div):
    def __init__(self, other=None, height=None, padding=5, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.add(raw(other)) # Logic to add child dominate tag
        self.height=height
        self.padding=padding
        self.__class__.__name__ = 'div'
        if self.height:
            self.update_height(self.height)
        if other:
            if not isinstance(other, list):
                self.add(other)
            else:
                for element in other:
                    self.add(element)

    def update_height(self, height):
        self.height = height
        self.set_attribute('style', 'height: {height:.0f}vh'.format(height=(100 - self.padding * 2) * self.height / 100))

    def add_class(self, new_cls):
        self.set_attribute('style', 'height: {height:.0f}vh'.format(height=(100 - self.padding * 2) * self.height / 100))
        self.attributes['class'] = self.attributes['class'] + ' ' + new_cls

    def add_class(self, new_cls):
        self.set_attribute('style', 'height: {height:.0f}vh'.format(height=(100 - self.padding * 2) * self.height / 100))
        self.attributes['class'] = self.attributes['class'] + ' ' + new_cls


class Col1(Col):
    def __init__(self, *args, **kwargs):
        super().__init__(cls='col-md-1', *args, **kwargs)


class Col2(Col):
    def __init__(self, *args, **kwargs):
        super().__init__(cls='col-md-2', *args, **kwargs)


class Col3(Col):
    def __init__(self, *args, **kwargs):
        super().__init__(cls='col-md-3', *args, **kwargs)


class Col4(Col):
    def __init__(self, *args, **kwargs):
        super().__init__(cls='col-md-4', *args, **kwargs)


class Col5(Col):
    def __init__(self, *args, **kwargs):
        super().__init__(cls='col-md-5', *args, **kwargs)


class Col6(Col):
    def __init__(self, *args, **kwargs):
        super().__init__(cls='col-md-6', *args, **kwargs)


class Col7(Col):
    def __init__(self, *args, **kwargs):
        super().__init__(cls='col-md-7', *args, **kwargs)


class Col8(Col):
    def __init__(self, *args, **kwargs):
        super().__init__(cls='col-md-8', *args, **kwargs)


class Col9(Col):
    def __init__(self, *args, **kwargs):
        super().__init__(cls='col-md-9', *args, **kwargs)


class Col10(Col):
    def __init__(self, *args, **kwargs):
        super().__init__(cls='col-md-10', *args, **kwargs)


class Col11(Col):
    def __init__(self, *args, **kwargs):
        super().__init__(cls='col-md-11', *args, **kwargs)


class Col12(Col):
    def __init__(self, *args, **kwargs):
        super().__init__(cls='col-md-12', *args, **kwargs)



# sam2=Col6(height=100)
#
# sam = Row()
# sam1 = Row()
# sam1.update_height(50)
# sam1.add(sam)
# sam1.add(sam2)
#
# with sam:
#     Row()
#
# sam2.render()
# sam2.add_class('col-sm-2')
#
# print(sam2)

# class Col1(Col):
#     def __init__(self, *args, **kwargs):
#         super().__init__(classes=["md-1"], *args, **kwargs)
#
#
# class Col2(Col):
#     def __init__(self, *args, **kwargs):
#         super().__init__(classes=["md-2"], *args, **kwargs)
#
#
# class Col3(Col):
#     def __init__(self, *args, **kwargs):
#         super().__init__(classes=["md-3"], *args, **kwargs)
#
#
# class Col4(Col):
#     def __init__(self, *args, **kwargs):
#         super().__init__(classes=["md-4"], *args, **kwargs)
#
#
# class Col5(Col):
#     def __init__(self, *args, **kwargs):
#         super().__init__(classes=["md-5"], *args, **kwargs)
#
#
# class Col6(Col):
#     def __init__(self, *args, **kwargs):
#         super().__init__(classes=["md-6"], *args, **kwargs)
#
#
# class Col7(Col):
#     def __init__(self, *args, **kwargs):
#         super().__init__(classes=["md-7"], *args, **kwargs)
#
#
# class Col8(Col):
#     def __init__(self, *args, **kwargs):
#         super().__init__(classes=["md-8"], *args, **kwargs)
#
#
# class Col9(Col):
#     def __init__(self, *args, **kwargs):
#         super().__init__(classes=["md-9"], *args, **kwargs)
#
#
# class Col10(Col):
#     def __init__(self, *args, **kwargs):
#         super().__init__(classes=["md-10"], *args, **kwargs)
#
#
# class Col11(Col):
#     def __init__(self, *args, **kwargs):
#         super().__init__(classes=["md-11"], *args, **kwargs)
#
#
# class Col12(Col):
#     def __init__(self, *args, **kwargs):
#         super().__init__(classes=["md-12"], *args, **kwargs)
#

class Dimension:
    def __init__(self, column):
        self.dim_replaced = column.replace(" ", "_").replace("(", "").replace(")", "")
        self.dimension_code = self.make_dimension(column)
        self.dimension_name = "{dim_replaced}_dimension".format(
            dim_replaced=self.dim_replaced
        )
        self.group_name = "{dim_replaced}_group".format(dim_replaced=self.dim_replaced)
        GLOBAL_DIMENSION_CODE.append(self.dimension_code)

    def make_dimension(self, column):
        dimension_string = """
            var {dim_replaced}_dimension = facts.dimension(function(d){{return d['{dim}'];}});
            var {dim_replaced}_group = {dim_replaced}_dimension.group();
        """
        return dimension_string.format(dim=column, dim_replaced=self.dim_replaced)
