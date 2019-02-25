from abc import ABCMeta, abstractmethod
from copy import copy
from dominate.tags import div

INDENTION = "    "
DIMENSION_SPACING = "\n" + INDENTION * 2


class BaseMixin(metaclass=ABCMeta):
    @abstractmethod
    def __init__(
        self,
        chartGroup=None,
        dimension=None,
        group=None,
        height=None,
        width=None,
        label=None,
        keyAccessor=None,
        valueAccessor=None,
        renderLabel=None,
        transitionDuration=None,
    ):
        self.chartGroup = chartGroup
        self.dimension = dimension
        self.group = group
        self.height = height
        self.width = width
        self.label = label
        self.valueAccessor = valueAccessor
        self.keyAccessor = keyAccessor
        self.renderLabel = renderLabel
        self.transitionDuration = transitionDuration


class CapMixin(BaseMixin, metaclass=ABCMeta):
    @abstractmethod
    def __init__(
        self,
        cap=None,
        othersGrouper=None,
        othersLabel=None,
        takeFront=None,
        *args,
        **kwargs,
    ):
        self.cap = cap
        self.othersGrouper = othersGrouper
        self.othersLabel = othersLabel
        self.takeFront = takeFront
        super().__init__(*args, **kwargs)


class ColorMixin(BaseMixin, metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, colorAccessor=None, colors=None, colorDomain=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.colorAccessor = colorAccessor
        self.colors = colors
        self.colorDomain = colorDomain


class MarginMixin(BaseMixin, metaclass=ABCMeta):
    @abstractmethod
    def __init__(
        self,
        margin_top=None,
        margin_right=None,
        margin_bottom=None,
        margin_left=None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.margin_top = margin_top
        self.margin_right = margin_right
        self.margin_bottom = margin_bottom
        self.margin_left = margin_left


class CoordinateGridMixin(ColorMixin, MarginMixin, metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, elasticY=None, x=None, y=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.elasticY = elasticY
        self.x = x
        self.y = y


class StackMixin(CoordinateGridMixin, metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class BubbleMixin(BaseMixin, metaclass=ABCMeta):
    @abstractmethod
    def __init__(
        self,
        maxBubbleRelativeSize=None,
        minRadius=None,
        minRadiusWithLabel=None,
        r=None,
        radiusValueAccessor=None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.maxBubbleRelativeSize = maxBubbleRelativeSize
        self.minRadius = minRadius
        self.minRadiusWithLabel = minRadiusWithLabel
        self.r = r
        self.radiusValueAccessor = radiusValueAccessor


class BarChart(StackMixin):
    def __init__(
        self,
        name,
        dimension,
        alwaysUseRounding=None,
        barPadding=None,
        centerBar=None,
        gap=None,
        outerPadding=None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.name = name
        self.dimension = dimension
        self.alwaysUseRounding = alwaysUseRounding
        self.barPadding = barPadding
        self.centerBar = centerBar
        self.gap = gap
        self.outerPadding = outerPadding

    @property
    def js_chart_code(self):
        dimension_string_list = [
            f'var bar_chart_{self.name.replace("-", "_")} = dc.barChart("#{self.name}")',
            f".dimension({self.dimension.dimension_name})",
            f".group({self.dimension.group_name})",
        ]

        axis_string_list = [f'bar_chart_{self.name.replace("-", "_")}']
        margin_string_list = [f'bar_chart_{self.name.replace("-", "_")}']

        if self.elasticY:
            dimension_string_list.append(f".elasticY(true)")

        if self.centerBar:
            dimension_string_list.append(f".centerBar(true)")

        if self.alwaysUseRounding:
            dimension_string_list.append(f".alwaysUseRounding(true)")

        if self.gap:
            dimension_string_list.append(f".gap({self.gap})")

        if self.width:
            dimension_string_list.append(f".width({self.width})")

        if self.height:
            dimension_string_list.append(f".height({self.height})")

        axis_string_list.append(f".x(d3.scaleLinear().domain([-25, 25]))")

        DIMENSION_FINAL = DIMENSION_SPACING.join(dimension_string_list) + ";"
        AXIS_FINAL = DIMENSION_SPACING.join(axis_string_list) + ";"

        if self.margin_left:
            margin_string_list.append(f".margins().left = {self.margin_left}")

        if self.margin_right:
            margin_string_list.append(f".margins().right = {self.margin_right}")

        if self.margin_top:
            margin_string_list.append(f".margins().top = {self.margin_top}")

        if self.margin_bottom:
            margin_string_list.append(f".margins().bottom = {self.margin_bottom}")

        if any(
            (self.margin_left, self.margin_right, self.margin_top, self.margin_bottom)
        ):
            MARGIN_FINAL = DIMENSION_SPACING.join(margin_string_list) + ";"
            return DIMENSION_FINAL + "\n" + AXIS_FINAL + "\n" + MARGIN_FINAL

        else:
            return DIMENSION_FINAL + "\n" + AXIS_FINAL

    def __str__(self):
        return self.js_chart_code

    def __repr__(self):
        return f'<BarChart: "#{self.name}">'


class ScatterPlot(CoordinateGridMixin):
    def __init__(
        self,
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
        symbolSize=None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.name = name
        self.dimension = dimension
        self.customSymbol = customSymbol
        self.emptySize = emptySize
        self.excludedColor = excludedColor
        self.excludedOpacity = excludedOpacity
        self.excludedSize = excludedSize
        self.existenceAccessor = existenceAccessor
        self.highlightedSize = highlightedSize
        self.symbol = symbol
        self.symbolSize = symbolSize

    @property
    def js_chart_code(self):

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
            dimension_string_list.append(
                f".existenceAccessor({self.existenceAccessor})"
            )

        if self.highlightedSize:
            dimension_string_list.append(f".highlightedSize({self.highlightedSize})")

        if self.symbol:
            dimension_string_list.append(f".symbol({self.symbol})")

        if self.symbolSize:
            dimension_string_list.append(f".symbolSize({self.symbolSize})")

        axis_string_list.append(f".x(d3.scaleLinear().domain([14, 20]))")

        DIMENSION_FINAL = DIMENSION_SPACING.join(dimension_string_list) + ";"
        AXIS_FINAL = DIMENSION_SPACING.join(axis_string_list) + ";"

        return DIMENSION_FINAL + "\n" + AXIS_FINAL

    def __str__(self):
        return self.js_chart_code

    def __repr__(self):
        return f'<ScatterPlot: "#{self.name}">'


class RowChart(CapMixin, ColorMixin, MarginMixin):
    def __init__(
        self,
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
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.name = name
        self.name_replaced = f'row_chart_{self.name.replace("-", "_")}'
        self.dimension = dimension
        self.elasticX = elasticX
        self.fixedBarHeight = fixedBarHeight
        self.gap = gap
        self.labelOffsetX = labelOffsetX
        self.labelOffsetY = labelOffsetY
        self.renderTitleLabel = renderTitleLabel
        self.titleLabelOffsetX = titleLabelOffsetX
        self.x = x
        self.xAxis = xAxis
        # self.xAxis()

    @property
    def js_chart_code(self):

        dimension_string_list = [
            f'var {self.name_replaced} = dc.rowChart("#{self.name}")',
        ]

        axis_string_list = [f'row_chart_{self.name.replace("-", "_")}']

        if self.width:
            dimension_string_list.append(f".width({self.width})")

        if self.height:
            dimension_string_list.append(f".height({self.height})")

        dimension_string_list.append(f".margins({{top: 20, left: 10, right: 10, bottom: 20}})")

        dimension_string_list.append(f".group({self.dimension.group_name})")
        dimension_string_list.append(f".dimension({self.dimension.dimension_name})")

        dimension_string_list.append(f".ordinalColors(['#3182bd','#6baed6','#9ecae1','#c6dbef','#dadaeb'])")
        dimension_string_list.append(".title(function(d){return d.value;})")


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
            dimension_string_list.append(
                f".titleLabelOffsetX({self.titleLabelOffsetX})"
            )

        if self.x:
            dimension_string_list.append(f".x({self.x})")

        if self.xAxis:
            axis_string_list.append(f".xAxis().{self.xAxis}")

        DIMENSION_FINAL = DIMENSION_SPACING.join(dimension_string_list) + ";"
        AXIS_FINAL = DIMENSION_SPACING.join(axis_string_list) + ";"

        DIMENSION_AND_AXIS = DIMENSION_FINAL + "\n" + AXIS_FINAL

        if self.label:
            self.label.chart_name = self.name_replaced
            if self.label.label_type == "key":
                return DIMENSION_AND_AXIS + self.label.key

        return DIMENSION_AND_AXIS

    # https://stackoverflow.com/questions/48338847/how-to-copy-a-class-instance-in-python

    def __str__(self):
        return self.js_chart_code

    def __repr__(self):
        return f'<RowChart: "#{self.name}">'


class PieChart(CapMixin, ColorMixin):
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
        self.name_replaced = f'pie_chart_{self.name.replace("-", "_")}'
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

        dimension_string_list = [
            f'var pie_chart_{self.name.replace("-", "_")} = dc.pieChart("#{self.name}")'
        ]

        if self.width:
            dimension_string_list.append(f".width({self.width})")

        if self.height:
            dimension_string_list.append(f".height({self.height})")

        if self.radius:
            dimension_string_list.append(f".radius({self.radius})")

        dimension_string_list.append(f".dimension({self.dimension.dimension_name})")
        dimension_string_list.append(f".group({self.dimension.group_name})")

        if self.renderLabel:
            dimension_string_list.append(".renderLabel(true)")

        if self.inner_radius:
            dimension_string_list.append(f".innerRadius({self.inner_radius})")

        if self.transitionDuration:
            dimension_string_list.append(f".transitionDuration({self.transitionDuration})")

        if self.colors:
            dimension_string_list.append(f".colors({self.colors})")

        if self.colorDomain:
            dimension_string_list.append(f".colorDomain({self.colorDomain})")

        if self.colorAccessor:
            dimension_string_list.append(".colorAccessor(function(d, i){return d.value;})")

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

        if self.label:
            self.label.chart_name = self.name_replaced
            if self.label.label_type == "percent":
                return (
                    DIMENSION_SPACING.join(dimension_string_list)
                    + ";"
                    + self.label.percent
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


class Label:
    def __init__(self, label_type=None, precision=2, chart_name=""):
        self.chart_name = chart_name
        self.label_type = label_type
        self.precision = precision

    @property
    def percent(self):
        printed_precision = "0" * self.precision

        func_name = f""".label(function(d){{
            if ({self.chart_name}.hasFilter() && !{self.chart_name}.hasFilter(d.key)) {{
                return d.key + ' (0%)';
            }}
            var label = d.key;
            if (all.value()) {{
                label += ' (' + Math.floor(d.value / all.value() * 100{printed_precision})/1{printed_precision} + '%)';
            }}
            return label;
            }});"""

        return self.chart_name + DIMENSION_SPACING + func_name


    @property
    def key(self):
        func_name = """.label(function(d){
            return d.key[0];
        });"""

        return self.chart_name + DIMENSION_SPACING + func_name


class BubbleChart(BubbleMixin, CoordinateGridMixin):
    """This is an implementation of the DCjs Bubble Chart.
    The documentation for how the DC methods work may be found at
    https://dc-js.github.io/dc.js/docs/html/dc.bubbleChart.html."""

    def __init__(self, name, dimension, width, height, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.dimension = dimension
        self.width = width
        self.height = height

    @property
    def js_chart_code(self):
        dimension_string_list = [
            f'var bubble_chart_{self.name.replace("-", "_")} = dc.bubbleChart("#{self.name}")',
            f".dimension({self.dimension.dimension_name})",
            f".group({self.dimension.group_name})",
        ]

        if self.width:
            dimension_string_list.append(f".width({self.width})")

        if self.height:
            dimension_string_list.append(f".height({self.height})")

        if self.colorAccessor:
            dimension_string_list.append(
                f".colorAccessor(function(d){{return d.value.{self.keyAccessor};}})"
            )

        if self.keyAccessor:
            dimension_string_list.append(
                f".keyAccessor(function(d){{return d.value.{self.keyAccessor};}})"
            )

        if self.valueAccessor:
            dimension_string_list.append(
                f".valueAccessor(function(d){{return d.value.{self.valueAccessor};}})"
            )

        if self.radiusValueAccessor:
            dimension_string_list.append(
                f".radiusValueAccessor(function(d){{return d.value.{self.radiusValueAccessor};}})"
            )

        if self.x:
            dimension_string_list.append(f".x(d3.scaleLinear().domain([-2500, 2500]))")

        if self.y:
            dimension_string_list.append(f".y(d3.scaleLinear().domain([-100, 100]))")

        if self.r:
            dimension_string_list.append(f".r(d3.scaleLinear().domain([0, 4000]))")

        dimension_string_list.append(f".margins({{top: 10, right: 50, bottom: 30, left: 40}})")
        dimension_string_list.append(f".elasticY(true)")
        dimension_string_list.append(f".elasticX(true)")
        dimension_string_list.append(f".colors(d3.schemeRdYlGn[9])")
        dimension_string_list.append(f".colorDomain([-500,500])")
        dimension_string_list.append(f".yAxisPadding(100)")
        dimension_string_list.append(f".xAxisPadding(500)")
        dimension_string_list.append(f".maxBubbleRelativeSize(0.3)")
        dimension_string_list.append(f".renderHorizontalGridLines(true)")
        dimension_string_list.append(f".renderVerticalGridLines(true)")
        dimension_string_list.append(f".xAxisLabel('Index Gain')")
        dimension_string_list.append(f".yAxisLabel('Index Gain %')")

        """
        var myChart = dc.bubbleChart("#chart")
        .width(1000)
        .height(300)
        .dimension(scatter_dimension)
        .group(scatter_group)
        .clipPadding(70)
        .colorAccessor(function(d){ return d.key[0];})
        .colors(colorbrewer.RdBu[6])
        
        .title(function(d){return 'x: ' + d.key[0] +', y:' + d.key[1]})
        .maxBubbleRelativeSize(0.05)
        .yAxisLabel("Tip Size")
        .renderHorizontalGridLines(true)
        .renderVerticalGridLines(true)
        .margins({top:40, bottom: 60, right: 80, left: 60});
        """

        return DIMENSION_SPACING.join(dimension_string_list) + ";"

    def __str__(self):
        return self.js_chart_code

    def __repr__(self):
        return f'<BubbleChart: "#{self.name}">'
