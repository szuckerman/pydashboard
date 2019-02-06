from abc import ABCMeta, abstractmethod
from copy import copy
from dominate.tags import div


class BaseMixin(metaclass=ABCMeta):
    @abstractmethod
    def __init__(
        self, chartGroup=None, dimension=None, group=None, height=None, width=None
    ):
        self.chartGroup = chartGroup
        self.dimension = dimension
        self.group = group
        self.height = height
        self.width = width



class CapMixin(BaseMixin, metaclass=ABCMeta):
    @abstractmethod
    def __init__(
        self, cap=None, othersGrouper=None, othersLabel=None, takeFront=None, *args, **kwargs
    ):
        self.cap = cap
        self.othersGrouper = othersGrouper
        self.othersLabel = othersLabel
        self.takeFront = takeFront
        super().__init__(*args, **kwargs)


class ColorMixin(BaseMixin, metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MarginMixin(BaseMixin, metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CoordinateGridMixin(ColorMixin, MarginMixin, metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ScatterPlot(CoordinateGridMixin):
    def __init__(self,
                 name,
                 dimension,
                 customSymbol=None,
                 emptySize=None,
                 excludedColor=None,
                 excludedOpacity=None,
                 excludedSize=None,
                 existenceAccessor=None,
                 highlightedSize=None,
                 symbol=None,
                 symbolSize=None):
        self.name=name
        self.dimension=dimension
        self.customSymbol=customSymbol
        self.emptySize=emptySize
        self.excludedColor=excludedColor
        self.excludedOpacity=excludedOpacity
        self.excludedSize=excludedSize
        self.existenceAccessor=existenceAccessor
        self.highlightedSize=highlightedSize
        self.symbol=symbol
        self.symbolSize=symbolSize

    @property
    def js_chart_code(self):
        INDENTION = "    "
        DIMENSION_SPACING = "\n" + INDENTION * 2

        dimension_string_list = [
            f'var scatter_plot_{self.name.replace("-", "_")} = dc.scatterPlot("#{self.name}")',
            f".dimension({self.dimension.dimension_name})",
            f".group({self.dimension.group_name})",
        ]

        axis_string_list = [f'scatter_plot_{self.name.replace("-", "_")}']

        if self.customSymbol:
            dimension_string_list.append(f".customSymbol({self.customSymbol})")

        if self.emptySize:
            dimension_string_list.append(f".emptySize({self.emptySize})")

        if self.excludedColor:
            dimension_string_list.append(f".excludedColor({self.excludedColor})")

        if self.excludedOpacity:
            dimension_string_list.append(f".excludedOpacity({self.excludedOpacity})")

        if self.excludedSize:
            dimension_string_list.append(f".excludedSize({self.excludedSize})")

        if self.existenceAccessor:
            dimension_string_list.append(f".existenceAccessor({self.existenceAccessor})")

        if self.highlightedSize:
            dimension_string_list.append(f".highlightedSize({self.highlightedSize})")

        if self.symbol:
            dimension_string_list.append(f".symbol({self.symbol})")

        if self.symbolSize:
            dimension_string_list.append(f".symbolSize({self.symbolSize})")

        axis_string_list.append(f".x(d3.scaleLinear().domain([14, 20]))")

        DIMENSION_FINAL = DIMENSION_SPACING.join(dimension_string_list) + ";"
        AXIS_FINAL = DIMENSION_SPACING.join(axis_string_list) + ";"

        return DIMENSION_FINAL + '\n' + AXIS_FINAL

    def __str__(self):
        return self.js_chart_code

    def __repr__(self):
        return f'<ScatterPlot: "#{self.name}">'


class RowChart(CapMixin, ColorMixin, MarginMixin):
    def __init__(self,
                 name,
                 dimension,
                 elasticX=None,
                 fixedBarHeight=None,
                 gap=None,
                 labelOffsetX=None,
                 labelOffsetY=None,
                 renderTitleLabel=None,
                 titleLabelOffsetX=None,
                 x=None,
                 xAxis=None,
                 # xAxis=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name=name
        self.dimension=dimension
        self.elasticX=elasticX
        self.fixedBarHeight=fixedBarHeight
        self.gap=gap
        self.labelOffsetX=labelOffsetX
        self.labelOffsetY=labelOffsetY
        self.renderTitleLabel=renderTitleLabel
        self.titleLabelOffsetX=titleLabelOffsetX
        self.x=x
        self.xAxis=xAxis
        # self.xAxis()

    @property
    def js_chart_code(self):
        INDENTION = "    "
        DIMENSION_SPACING = "\n" + INDENTION * 2

        dimension_string_list = [
            f'var row_chart_{self.name.replace("-", "_")} = dc.rowChart("#{self.name}")',
            f".dimension({self.dimension.dimension_name})",
            f".group({self.dimension.group_name})",
        ]

        axis_string_list = [f'row_chart_{self.name.replace("-", "_")}']


        if self.elasticX:
            dimension_string_list.append(f".elasticX(true)")

        if self.fixedBarHeight:
            dimension_string_list.append(f".fixedBarHeight({self.fixedBarHeight})")

        if self.gap:
            dimension_string_list.append(f".gap({self.gap})")

        if self.labelOffsetX:
            dimension_string_list.append(f".labelOffsetX({self.labelOffsetX})")

        if self.labelOffsetY:
            dimension_string_list.append(f".labelOffsetY({self.labelOffsetY})")

        if self.renderTitleLabel:
            dimension_string_list.append(f".renderTitleLabel({self.renderTitleLabel})")

        if self.titleLabelOffsetX:
            dimension_string_list.append(f".titleLabelOffsetX({self.titleLabelOffsetX})")

        if self.x:
            dimension_string_list.append(f".x({self.x})")

        if self.xAxis:
            axis_string_list.append(f".xAxis().{self.xAxis}")

        DIMENSION_FINAL = DIMENSION_SPACING.join(dimension_string_list) + ";"
        AXIS_FINAL = DIMENSION_SPACING.join(axis_string_list) + ";"

        return DIMENSION_FINAL + '\n' + AXIS_FINAL

    # https://stackoverflow.com/questions/48338847/how-to-copy-a-class-instance-in-python

    def __str__(self):
        return self.js_chart_code

    def __repr__(self):
        return f'<RowChart: "#{self.name}">'


class PieChart(CapMixin):
    """This is an implementation of the DCjs Pie Chart.
    The documentation for how the DC methods work may be found at
    https://dc-js.github.io/dc.js/docs/html/dc.pieChart.html."""

    def __init__(
        self,
        name,
        dimension,
        cx=None,
        cy=None,
        radius=None,
        inner_radius=None,
        externalLabels=None,
        slicesCap=None,
        drawPaths=None,
        emptyTitle="No Data",
        minAngleForLabel=None,
        externalRadiusPadding=None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.name = name
        self.dimension = dimension
        # self.html = div(id=name)

        # Methods from https://dc-js.github.io/dc.js/docs/html/dc.pieChart.html
        self.cx = cx
        self.cy = cy
        self.drawPaths = drawPaths
        self.emptyTitle = emptyTitle
        self.externalLabels = externalLabels
        self.externalRadiusPadding = externalRadiusPadding
        self.inner_radius = inner_radius
        self.minAngleForLabel = minAngleForLabel
        self.radius = radius
        self.slicesCap = slicesCap

    @property
    def js_chart_code(self):
        INDENTION = "    "
        DIMENSION_SPACING = "\n" + INDENTION * 2

        dimension_string_list = [
            f'var pie_chart_{self.name.replace("-", "_")} = dc.pieChart("#{self.name}")',
            f".dimension({self.dimension.dimension_name})",
            f".group({self.dimension.group_name})",
        ]

        if self.radius:
            dimension_string_list.append(f".radius({self.radius})")

        if self.inner_radius:
            dimension_string_list.append(f".innerRadius({self.inner_radius})")

        if self.externalLabels:
            dimension_string_list.append(f".externalLabels({self.externalLabels})")

        if self.slicesCap:
            dimension_string_list.append(f".slicesCap({self.slicesCap})")

        if self.cx:
            dimension_string_list.append(f".cx({self.cx})")

        if self.cy:
            dimension_string_list.append(f".cy({self.cy})")

        if self.minAngleForLabel:
            dimension_string_list.append(f".minAngleForLabel({self.minAngleForLabel})")

        if self.drawPaths:
            dimension_string_list.append(".drawPaths(true)")

        if self.emptyTitle != "No Data":
            dimension_string_list.append(f".emptyTitle({self.emptyTitle})")

        if self.externalRadiusPadding:
            dimension_string_list.append(
                f".externalRadiusPadding({self.externalRadiusPadding})"
            )

        return DIMENSION_SPACING.join(dimension_string_list) + ";"

    # def __len__(self):
    #     return len(self.html)
    #
    # def __copy__(self):
    #     self.normalizeArgs()
    #     return C(self.a, self.b, kwargs=self.kwargs)
    #
    # def normalizeArgs(self):
    #     if not hasattr(self, "args"):
    #         self.a = []
    #     if not hasattr(self, "b"):
    #         self.b = None
    #     if not hasattr(self, "kwargs"):
    #         self.kwargs = {}

    # https://stackoverflow.com/questions/48338847/how-to-copy-a-class-instance-in-python

    def __str__(self):
        return self.js_chart_code

    def __repr__(self):
        return f'<PieChart: "#{self.name}">'

