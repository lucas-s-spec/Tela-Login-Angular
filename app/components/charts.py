import reflex as rx
from app.states.dashboard_state import DashboardState
from app.components.chart_utils import TOOLTIP_PROPS, dark_mode_tooltip_style


def requests_evolution_chart() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Requisições no Período",
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
                        id="colorReqs",
                        x1="0",
                        y1="0",
                        x2="0",
                        y2="1",
                    )
                ),
                rx.recharts.x_axis(
                    data_key="date",
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
                    data_key="count",
                    name="Requisições",
                    stroke="#6366f1",
                    fill="url(#colorReqs)",
                    stroke_width=2,
                    active_dot={"r": 6, "strokeWidth": 0},
                    type_="monotone",
                ),
                data=DashboardState.requests_over_time,
                width="100%",
                height="100%",
                margin={"top": 10, "right": 10, "left": -10, "bottom": 0},
            ),
            class_name=f"h-[300px] w-full {dark_mode_tooltip_style()}",
        ),
        class_name="bg-white dark:bg-gray-900 p-6 rounded-3xl shadow-sm border border-gray-100 dark:border-gray-800",
    )


def tokens_by_assistant_chart() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Tokens por Assistente",
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
                    data_key="tokens",
                    name="Total Tokens",
                    fill="#8b5cf6",
                    radius=[4, 4, 0, 0],
                    bar_size=40,
                ),
                data=DashboardState.tokens_by_assistant,
                width="100%",
                height="100%",
                margin={"top": 10, "right": 10, "left": -10, "bottom": 0},
            ),
            class_name=f"h-[300px] w-full {dark_mode_tooltip_style()}",
        ),
        class_name="bg-white dark:bg-gray-900 p-6 rounded-3xl shadow-sm border border-gray-100 dark:border-gray-800",
    )