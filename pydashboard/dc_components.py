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
        title=None,
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
        self.title = title
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
    def __init__(
        self, colorAccessor=None, colors=None, colorDomain=None, *args, **kwargs
    ):
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
    def __init__(
        self,
        elasticX=True,
        elasticY=True,
        renderHorizontalGridLines=True,
        renderVerticalGridLines=True,
        xAxis=None,
        yAxis=None,
        xAxisPadding=None,
        yAxisPadding=None,
        xAxisLabel=None,
        yAxisLabel=None,
        xUnits=None,
        x=None,
        y=None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.elasticX = elasticX
        self.elasticY = elasticY
        self.renderHorizontalGridLines = renderHorizontalGridLines
        self.renderVerticalGridLines = renderVerticalGridLines
        self.xAxis = xAxis
        self.yAxis = yAxis
        self.xAxisPadding = xAxisPadding
        self.yAxisPadding = yAxisPadding
        self.xAxisLabel = xAxisLabel
        self.yAxisLabel = yAxisLabel
        self.xUnits = xUnits
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
        xAxis=None,
        yAxis=None,
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
        self.xAxis = xAxis
        self.yAxis = yAxis

    @property
    def js_chart_code(self):
        dimension_string_list = [
            f'var bar_chart_{self.name.replace("-", "_")} = dc.barChart("#{self.name}")'
        ]

        x_axis_string_list = [f'bar_chart_{self.name.replace("-", "_")}']
        y_axis_string_list = [f'bar_chart_{self.name.replace("-", "_")}']
        margin_string_list = [f'bar_chart_{self.name.replace("-", "_")}']

        if self.width:
            dimension_string_list.append(f".width({self.width})")

        if self.height:
            dimension_string_list.append(f".height({self.height})")

        dimension_string_list.append(
            ".margins({top: 10, right: 50, bottom: 30, left: 40})"
        )
        dimension_string_list.append(f".dimension({self.dimension.dimension_name})")
        dimension_string_list.append(f".group({self.dimension.group_name})")

        if self.elasticY:
            dimension_string_list.append(f".elasticY(true)")

        if self.centerBar:
            dimension_string_list.append(f".centerBar(true)")

        if self.gap:
            dimension_string_list.append(f".gap({self.gap})")

        dimension_string_list.append(".round(dc.round.floor)")

        if self.alwaysUseRounding:
            dimension_string_list.append(f".alwaysUseRounding(true)")

        dimension_string_list.append(f".renderHorizontalGridLines(true)")

        dimension_string_list.append(f".x(d3.scaleLinear().domain([-25, 25]))")

        dimension_string_list.append(
            """
                .filterPrinter(function (filters) {
            var filter = filters[0], s = '';
            s += numberFormat(filter[0]) + '% -> ' + numberFormat(filter[1]) + '%';
            return s;
        })
        """
        )

        if self.xAxis:
            x_axis_string_list.append(f".xAxis().{self.xAxis}")

        if self.yAxis:
            y_axis_string_list.append(f".yAxis().{self.yAxis}")

        DIMENSION_FINAL = DIMENSION_SPACING.join(dimension_string_list) + ";"

        X_AXIS_FINAL = (
            DIMENSION_SPACING.join(x_axis_string_list) + ";"
            if len(x_axis_string_list) > 1
            else ""
        )

        Y_AXIS_FINAL = (
            DIMENSION_SPACING.join(y_axis_string_list) + ";"
            if len(y_axis_string_list) > 1
            else ""
        )

        AXES_FINAL = X_AXIS_FINAL + DIMENSION_SPACING + Y_AXIS_FINAL

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
            return DIMENSION_FINAL + "\n" + AXES_FINAL + "\n" + MARGIN_FINAL

        else:
            return DIMENSION_FINAL + "\n" + AXES_FINAL

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
        AXES_FINAL = DIMENSION_SPACING.join(axis_string_list) + ";"

        return DIMENSION_FINAL + "\n" + AXES_FINAL

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

    @property
    def js_chart_code(self):

        dimension_string_list = [
            f'var {self.name_replaced} = dc.rowChart("#{self.name}")'
        ]

        axis_string_list = [f'row_chart_{self.name.replace("-", "_")}']

        if self.width:
            dimension_string_list.append(f".width({self.width})")

        if self.height:
            dimension_string_list.append(f".height({self.height})")

        dimension_string_list.append(
            f".margins({{top: 20, left: 10, right: 10, bottom: 20}})"
        )

        dimension_string_list.append(f".group({self.dimension.group_name})")
        dimension_string_list.append(f".dimension({self.dimension.dimension_name})")

        dimension_string_list.append(
            f".ordinalColors(['#3182bd','#6baed6','#9ecae1','#c6dbef','#dadaeb'])"
        )
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

        if self.label:
            dimension_string_list.append(f"{self.label}")

        if self.xAxis:
            axis_string_list.append(f".xAxis().{self.xAxis}")

        DIMENSION_FINAL = DIMENSION_SPACING.join(dimension_string_list) + ";"
        AXES_FINAL = DIMENSION_SPACING.join(axis_string_list) + ";"

        DIMENSION_AND_AXIS = DIMENSION_FINAL + "\n" + AXES_FINAL

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
            dimension_string_list.append(
                f".transitionDuration({self.transitionDuration})"
            )

        if self.colors:
            dimension_string_list.append(f".colors({self.colors})")

        if self.colorDomain:
            dimension_string_list.append(f".colorDomain({self.colorDomain})")

        if self.colorAccessor:
            dimension_string_list.append(
                ".colorAccessor(function(d, i){return d.value;})"
            )

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
            return (
                DIMENSION_SPACING.join(dimension_string_list)
                + ";"
                + getattr(self.label, self.label.label_type)
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


class BubbleChart(BubbleMixin, CoordinateGridMixin):
    """This is an implementation of the DCjs Bubble Chart.
    The documentation for how the DC methods work may be found at
    https://dc-js.github.io/dc.js/docs/html/dc.bubbleChart.html."""

    def __init__(self, name, dimension, width, height, margins=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.dimension = dimension
        self.width = width
        self.height = height
        self.margins = margins

    @property
    def js_chart_code(self):
        dimension_string_list = [
            f'var bubble_chart_{self.name.replace("-", "_")} = dc.bubbleChart("#{self.name}")'
        ]

        x_axis_string_list = [f'bubble_chart_{self.name.replace("-", "_")}']
        y_axis_string_list = [f'bubble_chart_{self.name.replace("-", "_")}']

        if self.width:
            dimension_string_list.append(f".width({self.width})")

        if self.height:
            dimension_string_list.append(f".height({self.height})")

        if self.transitionDuration:
            dimension_string_list.append(
                f".transitionDuration({self.transitionDuration})"
            )

        if self.margins:
            dimension_string_list.append(f".margins({self.margins})")

        # dimension_string_list.append(
        #     f".margins({{top: 10, right: 50, bottom: 30, left: 40}})"
        # )

        dimension_string_list.append(f".dimension({self.dimension.dimension_name})")
        dimension_string_list.append(f".group({self.dimension.group_name})")

        dimension_string_list.append(f".colors(d3.schemeRdYlGn[9])")
        dimension_string_list.append(f".colorDomain([-500,500])")

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

        if self.maxBubbleRelativeSize:
            dimension_string_list.append(
                f".maxBubbleRelativeSize({self.maxBubbleRelativeSize})"
            )

        if self.x:
            dimension_string_list.append(f".x({self.x})")

        if self.y:
            dimension_string_list.append(f".y({self.y})")

        if self.r:
            dimension_string_list.append(f".r({self.r})")

        if self.elasticX:
            dimension_string_list.append(f".elasticX(true)")

        if self.elasticY:
            dimension_string_list.append(f".elasticY(true)")

        if self.xAxisPadding:
            dimension_string_list.append(f".xAxisPadding({self.xAxisPadding})")

        if self.yAxisPadding:
            dimension_string_list.append(f".yAxisPadding({self.yAxisPadding})")

        if self.renderHorizontalGridLines:
            dimension_string_list.append(f".renderHorizontalGridLines(true)")

        if self.renderVerticalGridLines:
            dimension_string_list.append(f".renderVerticalGridLines(true)")

        if self.xAxisLabel:
            dimension_string_list.append(f".xAxisLabel('{self.xAxisLabel}')")

        if self.yAxisLabel:
            dimension_string_list.append(f".yAxisLabel('{self.yAxisLabel}')")

        if self.label:
            dimension_string_list.append(".renderLabel(true)")
            dimension_string_list.append(str(self.label))

        if self.title:
            dimension_string_list.append(".renderTitle(true)")
            dimension_string_list.append(self.title)

        if self.xAxis:
            x_axis_string_list.append(f".xAxis().{self.xAxis}")

        if self.yAxis:
            y_axis_string_list.append(f".yAxis().{self.yAxis}")

        X_AXIS_FINAL = (
            DIMENSION_SPACING.join(x_axis_string_list) + ";"
            if len(x_axis_string_list) > 1
            else ""
        )

        Y_AXIS_FINAL = (
            DIMENSION_SPACING.join(y_axis_string_list) + ";"
            if len(y_axis_string_list) > 1
            else ""
        )

        AXES_FINAL = X_AXIS_FINAL + DIMENSION_SPACING + Y_AXIS_FINAL
        DIMENSION_FINAL = DIMENSION_SPACING.join(dimension_string_list) + ";"

        if AXES_FINAL:
            return DIMENSION_FINAL + "\n" + AXES_FINAL

        else:
            return DIMENSION_FINAL

    def __str__(self):
        return self.js_chart_code

    def __repr__(self):
        return f'<BubbleChart: "#{self.name}">'


class LineChart(StackMixin):
    def __init__(
        self,
        name,
        dimension,
        transitionDuration=1000,
        elasticY=True,
        renderHorizontalGridLines=True,
        mouseZoomable=True,
        legend=True,
        brushOn=False,
        renderArea=False,
        margins=False,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.name = name
        self.dimension = dimension
        self.transitionDuration = transitionDuration
        self.elasticY = elasticY
        self.renderHorizontalGridLines = renderHorizontalGridLines
        self.mouseZoomable = mouseZoomable
        self.legend = legend
        self.brushOn = brushOn
        self.renderArea = renderArea
        self.margins = margins

    @property
    def js_chart_code(self):
        dimension_string_list = [
            f'var line_chart_{self.name.replace("-", "_")} = dc.lineChart("#{self.name}")'
        ]

        if self.renderArea:
            dimension_string_list.append(f".renderArea(true)")

        if self.width:
            dimension_string_list.append(f".width({self.width})")

        if self.height:
            dimension_string_list.append(f".height({self.height})")

        if self.transitionDuration:
            dimension_string_list.append(
                f".transitionDuration({self.transitionDuration})"
            )

        if self.margins:
            dimension_string_list.append(f".margins({self.margins})")

        dimension_string_list.append(f".dimension({self.dimension.dimension_name})")

        if self.mouseZoomable:
            dimension_string_list.append(".mouseZoomable(true)")

        dimension_string_list.append(f".rangeChart(volumeChart)")

        dimension_string_list.append(
            f".x(d3.scaleTime().domain([newDate(1985,0,1),newDate(2012,11,31)]))"
        )

        dimension_string_list.append(f".round(d3.timeMonth.round)")

        if self.xUnits:
            dimension_string_list.append(f".xUnits({self.xUnits})")

        if self.elasticY:
            dimension_string_list.append(".elasticY(true)")

        if self.renderHorizontalGridLines:
            dimension_string_list.append(f".renderHorizontalGridLines(true)")

        if self.legend:
            dimension_string_list.append(f".legend({self.legend})")

        if not self.brushOn:
            dimension_string_list.append(".brushOn(false)")

        if self.dimension.group_text:
            dimension_string_list.append(
                f".group({self.dimension.group_name}, '{self.dimension.group_text}')"
            )
        else:
            dimension_string_list.append(f".group({self.dimension.group_name})")

        if self.valueAccessor:
            dimension_string_list.append(
                f".valueAccessor(function(d){{return d.value.{self.valueAccessor};}})"
            )

        dimension_string_list.append(
            f".stack(monthlyMoveGroup,'MonthlyIndexMove', function(d) {{return d.value;}})"
        )

        dimension_string_list.append(
            """.title(function (d) {
            var value = d.value.avg ? d.value.avg : d.value;
            if (isNaN(value)) {
                value = 0;
            }
            return dateFormat(d.key) + '\n' + numberFormat(value);
        })"""
        )

        return DIMENSION_SPACING.join(dimension_string_list) + ";"

    def __str__(self):
        return self.js_chart_code


class Legend:
    def __init__(self, x=None, y=None, itemHeight=None, gap=None):
        self.x = x
        self.y = y
        self.itemHeight = itemHeight
        self.gap = gap

    def __str__(self):
        label_string = (
            f"dc.legend()"
            f".x({self.x})"
            f".y({self.y})"
            f".itemHeight({self.itemHeight})"
            f".gap({self.gap})"
        )
        return label_string


class Title:
    def _add_percentage(self, x):
        if "percentage(" in x:
            return " + '%'"
        else:
            return ")"

    def __init__(self, title, decimals=2):
        self.numberFormat = f"d3.format('.{decimals}f')"
        self.title_list = ["d.key"]
        self.title_list += [
            "'"
            + k
            + f"' + numberFormat(d.value.{v.replace('percentage(', '')}{self._add_percentage(v)}"
            for k, v in title.items()
        ]

        self.title_list_joined = '[' + ",".join(self.title_list) + "].join('\n')"

        self.title_list_joined = self.title_list_joined.replace("\n", r"\n")

    def __str__(self):
        return ".title(function(d) {" f"return {self.title_list_joined}" "})"


class Margin:
    def __init__(self, top=None, right=None, bottom=None, left=None):
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left

    def __str__(self):
        margin_string = f"{{top:{self.top},right:{self.right},bottom:{self.bottom},left:{self.left}}}"
        return margin_string


class ScaleLinear:
    def __init__(self, domain):
        self.domain = domain

    def __str__(self):
        domain_string = f"d3.scaleLinear().domain({self.domain})"
        return domain_string


class Label:
    def __init__(self, label_type=None, precision=2, chart_name=None, part=None):

        self.label_type = label_type
        self.precision = precision
        self.chart_name = chart_name
        self.part_string = f"[{part}]" if part is not None else ""

    @property
    def percent(self):
        printed_precision = "0" * self.precision

        self.printed_label = f"""{self.chart_name}.label(function(d){{
            if ({self.chart_name}.hasFilter() && !{self.chart_name}.hasFilter(d.key)) {{
                return d.key + ' (0%)';
            }}
            var label = d.key;
            if (all.value()) {{
                label += ' (' + Math.floor(d.value / all.value() * 100{printed_precision})/1{printed_precision} + '%)';
            }}
            return label;
            }});"""

        return self.printed_label

    @property
    def key(self):
        self.printed_label = (
            ".label(function(d){" f"return d.key{self.part_string};" "})"
        )

        return self.printed_label

    def __str__(self):
        return getattr(self, self.label_type)
