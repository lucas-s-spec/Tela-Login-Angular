import reflex as rx
from app.states.dashboard_state import DashboardState
from app.components.chart_utils import TOOLTIP_PROPS, dark_mode_tooltip_style


def sales_evolution_chart() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Evolução de Vendas",
            class_name="text-lg font-semibold text-gray-900 dark:text-white mb-4",
        ),
        rx.el.div(
            rx.recharts.area_chart(
                rx.recharts.cartesian_grid(
                    stroke_dasharray="3 3",
                    vertical=False,
                    class_name="stroke-gray-200 dark:stroke-gray-700",
                ),
                rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
                rx.el.svg.defs(
                    rx.el.svg.linear_gradient(
                        rx.el.svg.stop(
                            offset="5%", stop_color="#6366f1", stop_opacity=0.3
                        ),
                        rx.el.svg.stop(
                            offset="95%", stop_color="#6366f1", stop_opacity=0
                        ),
                        id="colorRevenue",
                        x1="0",
                        y1="0",
                        x2="0",
                        y2="1",
                    )
                ),
                rx.recharts.x_axis(
                    data_key="month",
                    axis_line=False,
                    tick_line=False,
                    tick_margin=10,
                    class_name="text-xs font-medium text-gray-500 dark:text-gray-400",
                    stroke="currentColor",
                ),
                rx.recharts.y_axis(
                    axis_line=False,
                    tick_line=False,
                    tick_margin=10,
                    class_name="text-xs font-medium text-gray-500 dark:text-gray-400",
                    stroke="currentColor",
                ),
                rx.recharts.area(
                    data_key="total_revenue",
                    name="Receita",
                    stroke="#6366f1",
                    fill="url(#colorRevenue)",
                    stroke_width=2,
                    active_dot={"r": 6, "strokeWidth": 0},
                    type_="monotone",
                ),
                data=DashboardState.sales_history,
                width="100%",
                height="100%",
                margin={"top": 10, "right": 10, "left": 20, "bottom": 0},
            ),
            class_name=f"h-[300px] w-full {dark_mode_tooltip_style()}",
        ),
        class_name="bg-white dark:bg-gray-900 p-6 rounded-3xl shadow-sm border border-gray-100 dark:border-gray-800",
    )


def product_bar_chart() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Vendas por Código",
            class_name="text-lg font-semibold text-gray-900 dark:text-white mb-4",
        ),
        rx.el.div(
            rx.recharts.bar_chart(
                rx.recharts.cartesian_grid(
                    stroke_dasharray="3 3",
                    vertical=False,
                    class_name="stroke-gray-200 dark:stroke-gray-700",
                ),
                rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
                rx.recharts.x_axis(
                    data_key="name",
                    axis_line=False,
                    tick_line=False,
                    tick_margin=10,
                    class_name="text-xs font-medium text-gray-500 dark:text-gray-400",
                    stroke="currentColor",
                ),
                rx.recharts.y_axis(
                    axis_line=False,
                    tick_line=False,
                    tick_margin=10,
                    class_name="text-xs font-medium text-gray-500 dark:text-gray-400",
                    stroke="currentColor",
                ),
                rx.recharts.bar(
                    data_key="value",
                    name="Qtd. Vendida",
                    fill="#8b5cf6",
                    radius=[4, 4, 0, 0],
                    bar_size=40,
                ),
                data=DashboardState.product_performance,
                width="100%",
                height="100%",
                margin={"top": 10, "right": 10, "left": -20, "bottom": 0},
            ),
            class_name=f"h-[300px] w-full {dark_mode_tooltip_style()}",
        ),
        class_name="bg-white dark:bg-gray-900 p-6 rounded-3xl shadow-sm border border-gray-100 dark:border-gray-800",
    )


def product_pie_chart() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Participação por Produto",
            class_name="text-lg font-semibold text-gray-900 dark:text-white mb-4",
        ),
        rx.el.div(
            rx.recharts.pie_chart(
                rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
                rx.recharts.pie(
                    data=DashboardState.product_share,
                    data_key="value",
                    name_key="name",
                    cx="50%",
                    cy="50%",
                    inner_radius=60,
                    outer_radius=80,
                    padding_angle=5,
                    stroke="none",
                    stroke_width=0,
                ),
                width="100%",
                height="100%",
            ),
            class_name=f"h-[300px] w-full flex items-center justify-center {dark_mode_tooltip_style()}",
        ),
        rx.el.div(
            rx.foreach(
                DashboardState.product_share,
                lambda item: rx.el.div(
                    rx.el.div(
                        class_name="w-3 h-3 rounded-full",
                        style={"backgroundColor": item["fill"]},
                    ),
                    rx.el.span(
                        item["name"],
                        class_name="text-sm text-gray-600 dark:text-gray-300",
                    ),
                    class_name="flex items-center gap-2",
                ),
            ),
            class_name="flex justify-center gap-6 mt-4",
        ),
        class_name="bg-white dark:bg-gray-900 p-6 rounded-3xl shadow-sm border border-gray-100 dark:border-gray-800",
    )