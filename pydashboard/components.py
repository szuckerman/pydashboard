from collections import deque

from dominate.tags import *
from dominate.util import raw, text
from flask import Flask, render_template
from jinja2 import Environment, FileSystemLoader
import pandas as pd
import tempfile
import webbrowser


env = Environment(
    loader=FileSystemLoader(
        "/Users/zucks/PycharmProjects/pydashboard/pydashboard/templates"
    )
)


GLOBAL_JS_CODE = []
GLOBAL_DIMENSION_CODE = []
DATA_COLUMNS = set()


def string_join(list_name):
    return "".join(str(i) for i in list_name)


def hello_world(x):
    return "hello %s!" % x


def is_number(s):
    """From: https://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float"""
    try:
        float(s)
        return True
    except ValueError:
        return False


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
        self.id = id
        self.height = height
        self.padding = padding
        self.__class__.__name__ = "div"
        self.add(text(self.id))
        if self.height:
            self.update_height(self.height)

    def update_height(self, height):
        self.height = height
        self.set_attribute(
            "style",
            "height: {height:.0f}vh".format(
                height=(100 - self.padding * 2) * self.height / 100
            ),
        )


# item = ChartElement(id="something", height=100)


class Dashboard:
    def __init__(self, *items, data=pd.DataFrame(), template=None):
        global DATA_COLUMNS
        self.data = data
        if items:
            self.add_graphs(*items)
        self.template = template
        self.outline_html = None
        if not data.empty:
            DATA_COLUMNS.update(set(data.columns))
        self.all_nodes = self._all_nodes()

    def add_template(self, *items):
        item_str = [raw(str(item)) for item in items]
        self.outline_html = div(item_str, {"class": "container"})

    def add_graphs(self, *items):
        self.items = items
        GLOBAL_JS_CODE = [str(item) for item in self.items]
        self.global_js_code = "\n".join(GLOBAL_JS_CODE)
        self.html = div(self.item_str, {"class": "container"})

    def add_graph_title(self, chart_object, title, add_reset_link=True, filter_language=' range: ', display_filter=False):

        reset_link = f'''<a class ="reset" href="javascript:{chart_object.name_replaced}.filterAll();dc.redrawAll();" style="display: none;"> reset </a>'''

        if display_filter:
            filter_language_section = f'<span class="reset">{filter_language}<span class="filter"></span></span>'
            reset_link = filter_language_section + reset_link

        return_node = {
            item for item in self.all_nodes if item.attributes.get("id") == chart_object.name
        }
        try:
            node = return_node.pop()
            node.add(title)
            if add_reset_link:
                node.add(raw(reset_link))
        except KeyError:
            return None

    def _all_nodes(self):
        """Borrowed from: https://codereview.stackexchange.com/a/135160"""
        visited, queue = set(), deque([self.template])
        while queue:
            vertex = queue.popleft()
            if hasattr(vertex, "children") and not isinstance(vertex, str):
                for node in vertex.children:
                    if node not in visited:
                        visited.add(node)
                        queue.append(node)
        return visited

    @property
    def item_str(self):
        return [raw(str(item)) for item in self.items]

    def show_chart_outlines(self):
        return str(self.html)

    def view_outlines(self):

        template = env.get_template("dashboard_outline.html")

        html_output = template.render(dashboard_outline=self.template)

        tmp = tempfile.NamedTemporaryFile(delete=False)
        path = tmp.name + ".html"
        f = open(path, "w")
        f.write(html_output)
        f.close()
        webbrowser.open("file://" + path)

    def view(self):
        template = env.get_template("dashboard.html")

        html_output = template.render(
            dimensions="\n".join(GLOBAL_DIMENSION_CODE),
            json_dat=self.data.to_json(orient="records"),
            chart_code=self.global_js_code,
            dashboard=self.template,
        )

        tmp = tempfile.NamedTemporaryFile(delete=False)
        path = tmp.name + ".html"
        f = open(path, "w")
        f.write(html_output)
        f.close()
        webbrowser.open("file://" + path)


class Row(div):
    def __init__(self, other=None, height=None, padding=5, *args, **kwargs):
        super().__init__(cls="row", *args, **kwargs)
        self.height = height
        self.padding = padding
        self.__class__.__name__ = "div"
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
        self.set_attribute(
            "style",
            "height: {height:.0f}vh".format(
                height=(100 - self.padding * 2) * self.height / 100
            ),
        )


class Container(div):
    def __init__(self, other=None, height=None, padding=5, *args, **kwargs):
        super().__init__(cls="container", *args, **kwargs)
        self.height = height
        self.padding = padding
        self.__class__.__name__ = "div"
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
        self.set_attribute(
            "style",
            "height: {height:.0f}vh".format(
                height=(100 - self.padding * 2) * self.height / 100
            ),
        )


class Col(div):
    def __init__(self, other=None, height=None, title=None, padding=5, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.add(raw(other)) # Logic to add child dominate tag
        self.height = height
        self.padding = padding
        self.title = title
        self.__class__.__name__ = "div"
        if self.height:
            self.update_height(self.height)
        if other:
            if not isinstance(other, list):
                self.add(other)
            else:
                for element in other:
                    self.add(element)

        if self.title:
            self.add(self.title)

    def update_height(self, height):
        self.height = height
        self.set_attribute(
            "style",
            "height: {height:.0f}vh".format(
                height=(100 - self.padding * 2) * self.height / 100
            ),
        )

    def add_class(self, new_cls):
        self.set_attribute(
            "style",
            "height: {height:.0f}vh".format(
                height=(100 - self.padding * 2) * self.height / 100
            ),
        )
        self.attributes["class"] = self.attributes["class"] + " " + new_cls


class Col1(Col):
    def __init__(self, *args, **kwargs):
        super().__init__(cls="col-md-1", *args, **kwargs)


class Col2(Col):
    def __init__(self, *args, **kwargs):
        super().__init__(cls="col-md-2", *args, **kwargs)


class Col3(Col):
    def __init__(self, *args, **kwargs):
        super().__init__(cls="col-md-3", *args, **kwargs)


class Col4(Col):
    def __init__(self, *args, **kwargs):
        super().__init__(cls="col-md-4", *args, **kwargs)


class Col5(Col):
    def __init__(self, *args, **kwargs):
        super().__init__(cls="col-md-5", *args, **kwargs)


class Col6(Col):
    def __init__(self, *args, **kwargs):
        super().__init__(cls="col-md-6", *args, **kwargs)


class Col7(Col):
    def __init__(self, *args, **kwargs):
        super().__init__(cls="col-md-7", *args, **kwargs)


class Col8(Col):
    def __init__(self, *args, **kwargs):
        super().__init__(cls="col-md-8", *args, **kwargs)


class Col9(Col):
    def __init__(self, *args, **kwargs):
        super().__init__(cls="col-md-9", *args, **kwargs)


class Col10(Col):
    def __init__(self, *args, **kwargs):
        super().__init__(cls="col-md-10", *args, **kwargs)


class Col11(Col):
    def __init__(self, *args, **kwargs):
        super().__init__(cls="col-md-11", *args, **kwargs)


class Col12(Col):
    def __init__(self, *args, **kwargs):
        super().__init__(cls="col-md-12", *args, **kwargs)


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
    def __init__(self, column, group=None, group_type=None, modifier=None):
        self.column = column
        self.group = group
        self.group_type = group_type
        self.dim_replaced = column.replace(" ", "_").replace("(", "").replace(")", "")
        # self.dimension_code = self.make_dimension(column)
        self.dimension_name = "{dim_replaced}_dimension".format(
            dim_replaced=self.dim_replaced
        )
        self.modifier = modifier if modifier else ''
        self.group_name = "{dim_replaced}_group".format(dim_replaced=self.dim_replaced)
        GLOBAL_DIMENSION_CODE.append(self.dimension_code)

    @property
    def dimension_code(self):

        dimension_string = [
            f"var {self.dim_replaced}_dimension = facts.dimension(function(d){{return d['{self.column}'];}});"
        ]

        if self.group_type == "sum":
            reduce_type = "reduceSum"
        elif self.group_type == "count":
            reduce_type = "reduceCount"

        if self.group:
            dimension_string.append(
                f'var {self.dim_replaced}_group = {self.dim_replaced}_dimension.group().{reduce_type}(function(d){{return d["{self.group}"]{self.modifier};}});'
            )
        else:
            dimension_string.append(
                f"var {self.dim_replaced}_group = {self.dim_replaced}_dimension.group();"
            )

        return "\n".join(dimension_string)

    def __str__(self):
        return self.dimension_code


class MultiDimension:
    def __init__(self, *args):

        self.dim_replaced = [
            column.replace(" ", "_").replace("(", "").replace(")", "")
            for column in args
        ]

        self.dim = "[" + ", ".join(f"d['{item}']" for item in self.dim_replaced) + "]"
        self.dim_replaced_together = "_".join(self.dim_replaced)
        self.dimension_name = f"{self.dim_replaced_together}_dimension"
        self.group_name = f"{self.dim_replaced_together}_group"
        GLOBAL_DIMENSION_CODE.append(self.dimension_code)

    @property
    def dimension_code(self):
        dimension_string = """
            var {dim_replaced_together}_dimension = facts.dimension(function(d){{return {dim};}});
            var {dim_replaced_together}_group = {dim_replaced_together}_dimension.group();
        """.format(
            dim_replaced_together=self.dim_replaced_together, dim=self.dim
        )
        return dimension_string


class NamedDimension2:
    def __init__(self, columns=None, groupby=None):

        self.columns = columns

        if isinstance(groupby, list):
            self.dim_replaced = [
                column.replace(" ", "_").replace("(", "").replace(")", "")
                for column in groupby
            ]

        else:
            self.dim_replaced = (
                groupby.replace(" ", "_").replace("(", "").replace(")", "")
            )

        if isinstance(self.dim_replaced, list):
            self.dim = (
                "[" + ", ".join(f"d['{item}']" for item in self.dim_replaced) + "]"
            )
            self.dim_replaced_together = "_".join(self.dim_replaced)

        else:
            self.dim = f"d['{self.dim_replaced}']"
            self.dim_replaced_together = self.dim_replaced

        self.dimension_name = f"{self.dim_replaced_together}_dimension"
        self.group_name = f"{self.dim_replaced_together}_group"
        GLOBAL_DIMENSION_CODE.append(self.dimension_code)

    @property
    def reduce_group_code(self):
        if isinstance(self.columns, dict):
            col_added = []
            for k, v in self.columns.items():
                has_division = ""
                if isinstance(v, VE):
                    if "/" in v.colname:
                        has_division = " : 0"
                    col_added.append(
                        "p.{k} += {v}{has_division};".format(
                            k=k, v=str(v)[1:-1], has_division=has_division
                        )
                    )
                else:
                    col_added.append("p.{k} += {v};".format(k=k, v=str(v)))

            col_removed = []
            for k, v in self.columns.items():
                has_division = ""
                if isinstance(v, VE):
                    if "/" in v.colname:
                        has_division = " : 0"
                    col_removed.append(
                        "p.{k} -= {v}{has_division};".format(
                            k=k, v=str(v)[1:-1], has_division=has_division
                        )
                    )
                else:
                    col_removed.append("p.{k} -= {v};".format(k=k, v=str(v)))

            col_init = [
                "{column}: 0".format(column=column) for column in self.columns.keys()
            ]

        else:
            col_added = [
                "p.{column} += v.{column};".format(column=column)
                for column in self.columns
            ]

            col_removed = [
                "p.{column} -= v.{column};".format(column=column)
                for column in self.columns
            ]

            col_init = ["{column}: 0".format(column=column) for column in self.columns]

        col_added_joined = "\n\t\t".join(col_added)

        col_removed_joined = "\n\t\t".join(col_removed)

        col_init_joined = ",\n\t\t".join(col_init)

        data_added = f"""
                function (p, v) {{
                    ++p.count;
                    {col_added_joined}
                    return p;
                }},
                """

        data_removed = f"""
                function (p, v) {{
                    --p.count;
                    {col_removed_joined}
                    return p;
                }},
                """

        data_init = f"""
                /* initialize p */
                function () {{
                    return {{
                        count: 0,
                        {col_init_joined}
                    }};
                }}
        """

        reduce_group_code = f"""
            var {self.dim_replaced_together}_group = {self.dim_replaced_together}_dimension.group().reduce(
                /* callback for when data is added to the current filter results */
                {data_added}
                /* callback for when data is removed from the current filter results */
                {data_removed}
                /* initialize p */
                {data_init}
            );
        """
        return reduce_group_code

    @property
    def dimension_code(self):
        dimension_string = """
            var {dim_replaced_together}_dimension = facts.dimension(function(d){{return {dim};}});
            {reduce_group_code}
        """.format(
            dim_replaced_together=self.dim_replaced_together,
            dim=self.dim,
            reduce_group_code=self.reduce_group_code,
        )
        return dimension_string

    def __str__(self):
        return self.reduce_group_code


class NamedDimension:
    def __init__(self, columns=None, groupby=None, group_text=None):

        self.columns = columns
        self.group_text = group_text

        if isinstance(groupby, list):
            self.dim_replaced = [
                column.replace(" ", "_").replace("(", "").replace(")", "")
                for column in groupby
            ]

        else:
            self.dim_replaced = (
                groupby.replace(" ", "_").replace("(", "").replace(")", "")
            )

        if isinstance(self.dim_replaced, list):
            self.dim = (
                "[" + ", ".join(f"d['{item}']" for item in self.dim_replaced) + "]"
            )
            self.dim_replaced_together = "_".join(self.dim_replaced)

        else:
            self.dim = f"d['{self.dim_replaced}']"
            self.dim_replaced_together = self.dim_replaced

        self.dimension_name = f"{self.dim_replaced_together}_dimension"
        self.group_name = f"{self.dim_replaced_together}_group"
        GLOBAL_DIMENSION_CODE.append(self.dimension_code)

    @property
    def reduce_group_code(self):

        for col in self.columns:
            col.add_or_remove = "add"
            col_added = [str(col) for col in self.columns]

        for col in self.columns:
            col.add_or_remove = "remove"
            col_removed = [str(col) for col in self.columns]

        col_init = ["{column}: 0".format(column=col.column) for col in self.columns]

        col_added_joined = "\n\t\t".join(col_added)

        col_removed_joined = "\n\t\t".join(col_removed)

        col_init_joined = ",\n\t\t".join(col_init)

        data_added = (
            ""
            "function (p, v) {"
            "    ++p.count;"
            f"    {col_added_joined}"
            "    return p;"
            "},"
        )

        data_removed = (
            ""
            "function (p, v) {"
            "    --p.count;"
            f"    {col_removed_joined}"
            "    return p;"
            "},"
        )

        data_init = (
            ""
            "function () {"
            "    return {"
            "        count: 0,"
            f"        {col_init_joined}"
            "    };"
            "}"
        )

        reduce_group_code = f"""
            var {self.dim_replaced_together}_group = {self.dim_replaced_together}_dimension.group().reduce(
                /* callback for when data is added to the current filter results */
                {data_added}
                /* callback for when data is removed from the current filter results */
                {data_removed}
                /* initialize p */
                {data_init}
                );
        """
        return reduce_group_code

    @property
    def dimension_code(self):
        dimension_string = """
            var {dim_replaced_together}_dimension = facts.dimension(function(d){{return {dim};}});
            {reduce_group_code}
        """.format(
            dim_replaced_together=self.dim_replaced_together,
            dim=self.dim,
            reduce_group_code=self.reduce_group_code,
        )
        return dimension_string

    def __str__(self):
        return self.reduce_group_code


def _is_str(x):
    col_set = {
        "date",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "oi",
        "change",
        "absGain",
        "fluctuation",
        "sumIndex",
    }
    if isinstance(x, str):
        if x in col_set:
            return "v." + x
        return "p." + x
    else:
        return str(x)


class Divide:
    def __init__(self, numerator=None, denominator=None):
        self.numerator = _is_str(numerator)
        self.denominator = _is_str(denominator)
        self.returned_string = (
            f"{self.denominator} ? {self.numerator} / {self.denominator} : 0;"
        )

    def __str__(self):
        return self.returned_string

    def __repr__(self):
        return f"<Divide: {self.numerator}/{self.denominator}>"


class Multiply:
    def __init__(self, *args):
        str_args = (_is_str(arg) for arg in args)
        self.returned_string = " * ".join(str_args)

    def __str__(self):
        return self.returned_string

    def __repr__(self):
        return f"<Multiply: {self.returned_string}>"


class Subtract:
    def __init__(self, *args):
        str_args = (_is_str(arg) for arg in args)
        self.returned_string = " - ".join(str_args)

    def __str__(self):
        return self.returned_string

    def __repr__(self):
        return f"<Subtract: {self.returned_string}>"


class Abs:
    def __init__(self, arg):
        self.arg = arg
        self.returned_string = f"Math.abs({self.arg})"

    def __str__(self):
        return self.returned_string

    def __repr__(self):
        return f"<Abs: {self.returned_string}>"


class Add:
    def __init__(self, *args):
        str_args = (_is_str(arg) for arg in args)
        self.returned_string = " + ".join(str_args)

    def __str__(self):
        return self.returned_string

    def __repr__(self):
        return f"<Add: {self.returned_string}>"


class VC:
    def __init__(self, colname, fix_zero_division=False):
        self.colname = colname
        self.fix_zero_division = fix_zero_division

    @property
    def columns(self):
        return DATA_COLUMNS

    @property
    def col_type(self):
        if isinstance(self.colname, str):
            if self.colname in DATA_COLUMNS:
                return "v."
            else:
                return "p."
        else:
            return None

    def in_data_columns(self, col):
        if col in DATA_COLUMNS:
            return "v." + col
        else:
            return "p." + col

    def __add__(self, other):
        if other.col_type:
            if isinstance(other, VC):
                return VE(
                    [
                        "(",
                        self.col_type,
                        self.colname,
                        " + ",
                        other.col_type,
                        other.colname,
                        ")",
                    ]
                )
            else:
                return VE(["(", self.col_type, self.colname, " + ", other, ")"])
        else:
            return VE(["(", self.col_type, self.colname, " + ", other.colname, ")"])

    def __sub__(self, other):
        if other.col_type:
            if isinstance(other, VC):
                return VE(
                    [
                        "(",
                        self.col_type,
                        self.colname,
                        " - ",
                        other.col_type,
                        other.colname,
                        ")",
                    ]
                )
            else:
                return VE(["(", self.col_type, self.colname, " - ", other, ")"])
        else:
            return VE(["(", self.col_type, self.colname, " - ", other.colname, ")"])

    def __mul__(self, other):
        if other.col_type:
            if isinstance(other, VC):
                return VE(
                    [
                        "(",
                        self.col_type,
                        self.colname,
                        " * ",
                        other.col_type,
                        other.colname,
                        ")",
                    ]
                )
            else:
                return VE(["(", self.col_type, self.colname, " * ", other, ")"])
        else:
            return VE(["(", self.col_type, self.colname, " * ", other.colname, ")"])

    def __abs__(self):
        return VE(["(", "Math.abs(", self.col_type, self.colname, ")", ")"])

    def __truediv__(self, other):
        if other.col_type:
            if isinstance(other, VC):
                denominator = [other.col_type, other.colname]
            else:
                denominator = [other]
        else:
            denominator = [other.colname]
        initial_str = [self.col_type, self.colname, " / "] + denominator
        if self.fix_zero_division or other.fix_zero_division:
            return VE(denominator + [" ? ", "("] + initial_str + [")", " : ", '0'])
        return VE(["("] + initial_str + [")"])

    __floordiv__ = __truediv__

    def __str__(self):
        return string_join((self.col_type, self.colname))


class VE:
    def __init__(self, vc_list, colname=None, fix_zero_division=False):
        self.vc_list = vc_list
        self.colname = colname
        self.fix_zero_division = fix_zero_division
        self.col_type = None

    def __str__(self):
        return string_join(self.vc_list)

    def __add__(self, other):
        if other.col_type:
            if isinstance(other, VC):
                return VE(
                    ["(", *self.vc_list, " + ", other.col_type, other.colname, ")"]
                )
            else:
                return VE(["(", *self.vc_list, " + ", other, ")"])
        else:
            return VE(["(", *self.vc_list, " + ", other.colname, ")"])

    def __sub__(self, other):
        if other.col_type:
            if isinstance(other, VC):
                return VE(
                    ["(", *self.vc_list, " - ", other.col_type, other.colname, ")"]
                )
            else:
                return VE(["(", *self.vc_list, " - ", other, ")"])
        else:
            return VE(["(", *self.vc_list, " - ", other.colname, ")"])

    def __mul__(self, other):
        if other.col_type:
            if isinstance(other, VC):
                return VE(
                    ["(", *self.vc_list, " * ", other.col_type, other.colname, ")"]
                )
            else:
                return VE(["(", *self.vc_list, " * ", other, ")"])
        else:
            return VE(["(", *self.vc_list, " * ", other.colname, ")"])

    def __abs__(self):
        if self.col_type:
            return VE(["(", "Math.abs(", self.col_type, *self.vc_list, ")", ")"])
        else:
            return VE(["(", "Math.abs(", *self.vc_list[1:-1], ")", ")"])

    def __round__(self):
        if self.col_type:
            return VE(["(", "Math.round(", self.col_type, *self.vc_list, ")", ")"])
        else:
            # return VE(["(", "Math.round(", *self.vc_list[1:-1], ")", ")"])
            return VE(["(", "Math.round(", *self.vc_list, ")", ")"])

    def __truediv__(self, other):
        if other.col_type:
            if isinstance(other, VC):
                denominator = [other.col_type, other.colname]
            else:
                denominator = [other]
        else:
            denominator = [other.colname]
        initial_str = self.vc_list + [" / "] + denominator
        if is_number(string_join(denominator)):
            return VE(["("] + initial_str + [")"])
        else:
            if self.fix_zero_division or other.fix_zero_division:
                return VE(denominator + [" ? ", "("] + initial_str + [")", " : 0"])
            return VE(["("] + initial_str + [")", " : 0"])

    __floordiv__ = __truediv__


class VS:
    def __init__(self, column, statement, add_or_remove=None, fix_zero_division=False):
        self.statement = statement
        self.column = column
        self.add_or_remove = add_or_remove
        self.fix_zero_division = fix_zero_division
        self.divisor = (
            str(self.statement).split("?")[0].strip()
            if "?" in str(self.statement)
            else "aa"
        )
        self.divisor_parenthesis = self.divisor[0] == "(" and self.divisor[-1] == ")"

    def add_or_remove_semicolon(self, statement):
        if ';' in str(statement) and str(statement)[-1] != ';':
            new_statement = statement.replace(';', '')
            new_statement += ';'
            return new_statement
        else:
            return statement + ';'

    def move_colon_zero_to_end(self, equation):
        colon_zero = ' : 0'
        colon_zero_parenthesis = ' : 0)'

        if colon_zero_parenthesis in equation:
            new_equation = equation.replace(colon_zero_parenthesis, '')
            return new_equation + colon_zero_parenthesis

        elif colon_zero in equation:
            new_equation = equation.replace(colon_zero, '')
            return new_equation + colon_zero

        else:
            return equation

    @property
    def make_statement(self):
        if self.divisor_parenthesis:
            return_string = (
                "p."
                + self.column
                + self.plus_or_minus(self.statement, self.add_or_remove)
                + "= "
                + self.add_or_remove_semicolon(self.move_colon_zero_to_end(str(self.statement)))
                # + ";"
            )
        else:
            if str(self.statement)[0] == "(" and str(self.statement)[-1] == ")":
                return_string = (
                    "p."
                    + self.column
                    + self.plus_or_minus(self.statement, self.add_or_remove)
                    + "= "
                    + self.add_or_remove_semicolon(self.move_colon_zero_to_end(str(self.statement)[1:-1]))
                    # + ";"
                )
            else:
                return_string = (
                    "p."
                    + self.column
                    + self.plus_or_minus(self.statement, self.add_or_remove)
                    + "= "
                    + self.add_or_remove_semicolon(self.move_colon_zero_to_end(str(self.statement)))
                    # + ";"
                )

        # if "?" in return_string:
        #     if ":" not in return_string:
        #         if 'Math.round(' in return_string or 'Math.abs(' in return_string:
        #             return_string = return_string[:-1]
        #             return_string += " : 0);"
        #         else:
        #             return_string = return_string[:-1]
        #             return_string += " : 0;"
        #     else:
        #         return_string = return_string[:-1]
        #         return_string += " : 0;"
        # else:
        #     return_string = return_string[:-1]
        #     return_string += " : 0;"

        return return_string

    def plus_or_minus(self, equation, equation_type=None):
        plus_or_minus = " "
        if "v." in str(equation):
            if equation_type == "add":
                plus_or_minus = " +"
            else:
                plus_or_minus = " -"
        return plus_or_minus

    def __str__(self):
        return self.make_statement


def plus_or_minus(equation, equation_type):
    plus_or_minus = ""
    if "v." in str(equation):
        if equation_type == "added":
            plus_or_minus = "+"
        else:
            plus_or_minus = "-"
    return plus_or_minus


class VirtualColumn:
    def __init__(self, col_name, col_value):
        self.col_name = col_name
        self.col_value = col_value
        self.returned_string = f"p.{col_name} += {self.col_value}"

    @property
    def columns(self):
        return DATA_COLUMNS

    def __str__(self):
        return self.returned_string

    def __repr__(self):
        return f"<VirtualColumn: {self.returned_string}>"
