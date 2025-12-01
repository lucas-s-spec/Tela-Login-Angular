import reflex as rx
from app.states.auth_state import AuthState
from app.states.dashboard_state import DashboardState
from app.components.auth_views import theme_toggle
from app.components.charts import requests_evolution_chart, tokens_by_assistant_chart


def kpi_card(
    title: str, value: str, icon: str, color: str, trend: str = ""
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(icon, class_name=f"w-6 h-6 {color}"),
                class_name="p-3 bg-gray-50 dark:bg-gray-800 rounded-xl",
            ),
            rx.cond(
                trend,
                rx.el.span(
                    trend,
                    class_name="text-xs font-medium text-emerald-600 bg-emerald-50 dark:bg-emerald-900/30 px-2 py-1 rounded-lg",
                ),
            ),
            class_name="flex justify-between items-start mb-4",
        ),
        rx.el.div(
            rx.el.p(
                title,
                class_name="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1",
            ),
            rx.el.h3(
                value, class_name="text-2xl font-bold text-gray-900 dark:text-white"
            ),
        ),
        class_name="bg-white dark:bg-gray-900 p-6 rounded-3xl shadow-sm border border-gray-100 dark:border-gray-800 hover:shadow-md transition-shadow duration-300",
    )


def filters_section() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.label(
                "Período",
                class_name="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1",
            ),
            rx.el.select(
                rx.el.option("Hoje", value="1"),
                rx.el.option("Últimos 7 dias", value="7"),
                rx.el.option("Últimos 30 dias", value="30"),
                value=DashboardState.selected_period,
                on_change=DashboardState.set_period,
                class_name="bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white text-sm rounded-lg focus:ring-indigo-500 focus:border-indigo-500 block w-full p-2.5",
            ),
            class_name="w-full sm:w-48",
        ),
        rx.el.div(
            rx.el.label(
                "Assistente",
                class_name="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1",
            ),
            rx.el.select(
                rx.el.option("Todos", value="Todos"),
                rx.foreach(
                    DashboardState.assistant_options,
                    lambda opt: rx.el.option(opt["label"], value=opt["value"]),
                ),
                value=DashboardState.selected_assistant_id,
                on_change=DashboardState.set_assistant_filter,
                class_name="bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white text-sm rounded-lg focus:ring-indigo-500 focus:border-indigo-500 block w-full p-2.5",
            ),
            class_name="w-full sm:w-64",
        ),
        class_name="flex flex-col sm:flex-row gap-4 mb-6 p-4 bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 shadow-sm",
    )


def summary_table() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Detalhamento por Assistente",
            class_name="text-lg font-semibold text-gray-900 dark:text-white mb-4 px-2",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Assistente",
                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Total Reqs",
                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Tokens Input",
                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Tokens Output",
                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Total Tokens",
                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Créditos Restantes",
                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                    ),
                    class_name="bg-gray-50 dark:bg-gray-800",
                ),
                rx.el.tbody(
                    rx.foreach(
                        DashboardState.assistants_summary,
                        lambda row: rx.el.tr(
                            rx.el.td(
                                rx.el.span(
                                    row["name"],
                                    class_name="font-medium text-gray-900 dark:text-white",
                                ),
                                class_name="px-6 py-4 whitespace-nowrap text-sm",
                            ),
                            rx.el.td(
                                row["reqs"],
                                class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400",
                            ),
                            rx.el.td(
                                row["input"],
                                class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400",
                            ),
                            rx.el.td(
                                row["output"],
                                class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400",
                            ),
                            rx.el.td(
                                rx.el.span(
                                    row["total"],
                                    class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800 dark:bg-indigo-900 dark:text-indigo-200",
                                ),
                                class_name="px-6 py-4 whitespace-nowrap text-sm",
                            ),
                            rx.el.td(
                                row["remaining"],
                                class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400",
                            ),
                            class_name="border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors",
                        ),
                    ),
                    class_name="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-800",
                ),
                class_name="min-w-full divide-y divide-gray-200 dark:divide-gray-800 table-auto",
            ),
            class_name="overflow-x-auto rounded-3xl border border-gray-100 dark:border-gray-800 shadow-sm",
        ),
        class_name="mt-8",
    )


def dashboard_view() -> rx.Component:
    return rx.el.div(
        rx.el.header(
            rx.el.div(
                rx.el.h1(
                    "Dashboard Geral",
                    class_name="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white",
                ),
                rx.el.div(
                    rx.el.span(
                        "Bem-vindo, ", class_name="text-gray-500 dark:text-gray-400"
                    ),
                    rx.el.span(
                        rx.cond(
                            AuthState.user_profile,
                            AuthState.user_profile["nome"],
                            "Administrador",
                        ),
                        class_name="font-semibold text-gray-900 dark:text-white",
                    ),
                    class_name="text-sm mt-1",
                ),
                class_name="flex flex-col",
            ),
            class_name="flex flex-col md:flex-row md:justify-between md:items-center gap-4 mb-8",
        ),
        filters_section(),
        rx.el.div(
            kpi_card(
                "Total de Assistentes",
                DashboardState.total_assistants.to_string(),
                "bot",
                "text-emerald-500",
            ),
            kpi_card(
                "Requisições (Período)",
                DashboardState.total_requests.to_string(),
                "zap",
                "text-blue-500",
            ),
            kpi_card(
                "Tokens Consumidos",
                DashboardState.total_tokens.to_string(),
                "cpu",
                "text-purple-500",
            ),
            kpi_card(
                "Custo Estimado",
                DashboardState.total_cost_estimated,
                "dollar-sign",
                "text-orange-500",
                "~ estimativa",
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8",
        ),
        rx.el.div(
            rx.el.div(requests_evolution_chart(), class_name="lg:col-span-1"),
            rx.el.div(tokens_by_assistant_chart(), class_name="lg:col-span-1"),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-6",
        ),
        summary_table(),
        class_name="w-full animate-fade-in pb-20",
    )