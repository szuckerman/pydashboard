from dominate.tags import *
from dominate.util import raw
from flask import Flask, render_template

GLOBAL_JS_CODE = []


def hello_world(x):
    return "hello %s!" % x


class Row:
    def __init__(self, *args):
        self.children = args
        # if type(classes) == str:
        #     self.classname = classes
        # else:
        #     self.classname = " ".join("row-" + item for item in classes)
        self.tags = {"class": "row"}
        # self.children = children if children else []
        self.html = div(**self.tags)
        self._add_child_elements()

    def __repr__(self):
        return "<Row: {num_children} children>".format(num_children=len(self.children))

    def __str__(self):
        return str(self.html)

    def _add_child_elements(self):
        if self.children:
            for child in self.children:
                self.html.add(child.html)

    def __gt__(self, other):
        self.children.append(other.html)
        self.html.add(other.html)
        return self

    def __iadd__(self, other):
        self.children.append(other.html)
        self.html.add(other.html)
        return self


class Col:
    def __init__(self, children=None, classes=None, name=None):
        self.classes = classes
        self.classname = " ".join("col-" + item for item in classes)
        self.tags = {"class": self.classname}
        self.children = self._instantiate_children(children)
        self.html = div(**self.tags)
        self._add_child_elements()

    def _instantiate_children(self, children):
        if type(children) == list:
            return children
        elif len(children) > 0:
            return [children]
        else:
            return []

    def __repr__(self):
        return "<{cls}: {classname}, {num_children} children>".format(
            cls=__class__.__name__,
            classname=self.classname,
            num_children=len(self.children),
        )

    def __str__(self):
        return str(self.html)

    def _add_child_elements(self):
        if self.children:
            for child in self.children:
                if type(child) == str:
                    self.html.add(raw(child))
                else:
                    self.html.add(child.html)
                if hasattr(child, "js_chart_code"):
                    GLOBAL_JS_CODE.append(child.js_chart_code)

    def __gt__(self, other):
        self.children.append(other.html)
        self.html.add(other.html)
        return self

    def __lt__(self, other):
        self.children.append(other.html)
        self.html.add(other.html)
        return self

    def __iadd__(self, other):
        self.children.append(other.html)
        self.html.add(other.html)
        return self

    def __getitem__(self, index):
        return self.children[index]


class ChartElement:
    def __init__(self, name=None, height=None, cls=None, id=None):
        self.name = name
        self.id = id
        self.height = height
        self.cls = cls
        self.tags = {"id": self.name}
        if height:
            self.tags["style"] = "height: {height}vh".format(height=self.height)
        if cls:
            self.tags["class"] = self.cls
        self.html = div(self.name, **self.tags)

    def __str__(self):
        return str(self.html)

    def __len__(self):
        return 1


class Dashboard:
    def __init__(self, *items):
        item_str = [raw(str(item)) for item in items]
        self.html = div(item_str, {"class": "container"})

    def show_chart_outlines(self):
        return str(self.html)

    def run_outlines(self, host="127.0.0.1", port=5000, debug=False):
        app = Flask(__name__)

        @app.route("/")
        def index():
            return render_template("div_test.html", div_test=self.show_chart_outlines())

        app.run(host=host, port=port, debug=debug)


class Col1(Col):
    def __init__(self, *args, **kwargs):
        super().__init__(classes=["md-1"], *args, **kwargs)


class Col2(Col):
    def __init__(self, *args, **kwargs):
        super().__init__(classes=["md-2"], *args, **kwargs)


class Col3(Col):
    def __init__(self, *args, **kwargs):
        super().__init__(classes=["md-3"], *args, **kwargs)


class Col4(Col):
    def __init__(self, *args, **kwargs):
        super().__init__(classes=["md-4"], *args, **kwargs)


class Col5(Col):
    def __init__(self, *args, **kwargs):
        super().__init__(classes=["md-5"], *args, **kwargs)


class Col6(Col):
    def __init__(self, *args, **kwargs):
        super().__init__(classes=["md-6"], *args, **kwargs)


class Col7(Col):
    def __init__(self, *args, **kwargs):
        super().__init__(classes=["md-7"], *args, **kwargs)


class Col8(Col):
    def __init__(self, *args, **kwargs):
        super().__init__(classes=["md-8"], *args, **kwargs)


class Col9(Col):
    def __init__(self, *args, **kwargs):
        super().__init__(classes=["md-9"], *args, **kwargs)


class Col10(Col):
    def __init__(self, *args, **kwargs):
        super().__init__(classes=["md-10"], *args, **kwargs)


class Col11(Col):
    def __init__(self, *args, **kwargs):
        super().__init__(classes=["md-11"], *args, **kwargs)


class Col12(Col):
    def __init__(self, *args, **kwargs):
        super().__init__(classes=["md-12"], *args, **kwargs)
