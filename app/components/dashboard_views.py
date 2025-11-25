import reflex as rx
from app.states.auth_state import AuthState
from app.states.dashboard_state import DashboardState
from app.components.auth_views import theme_toggle
from app.components.charts import (
    sales_evolution_chart,
    product_bar_chart,
    product_pie_chart,
)


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


def dashboard_view() -> rx.Component:
    return rx.el.div(
        theme_toggle(),
        rx.el.div(
            rx.el.header(
                rx.el.div(
                    rx.el.h1(
                        "Dashboard de Vendas",
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
                rx.el.button(
                    rx.icon("log-out", class_name="w-5 h-5 mr-2"),
                    "Sair",
                    on_click=AuthState.logout,
                    class_name="flex items-center px-4 py-2 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-gray-700 dark:text-gray-200 rounded-xl hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors shadow-sm font-medium",
                ),
                class_name="flex flex-col md:flex-row md:justify-between md:items-center gap-4 mb-8",
            ),
            rx.el.div(
                kpi_card(
                    "Vendas Totais",
                    DashboardState.total_sales,
                    "dollar-sign",
                    "text-emerald-500",
                    "+12.5%",
                ),
                kpi_card(
                    "Itens Vendidos",
                    DashboardState.total_items.to_string(),
                    "shopping-bag",
                    "text-blue-500",
                    "+8.2%",
                ),
                kpi_card(
                    "Vendas do Mês",
                    DashboardState.monthly_sales,
                    "calendar",
                    "text-purple-500",
                    "+2.4%",
                ),
                kpi_card(
                    "Ticket Médio",
                    DashboardState.avg_ticket,
                    "trending-up",
                    "text-orange-500",
                    "-1.1%",
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8",
            ),
            rx.el.div(
                rx.el.div(sales_evolution_chart(), class_name="lg:col-span-2"),
                rx.el.div(product_bar_chart(), class_name="col-span-1"),
                rx.el.div(product_pie_chart(), class_name="col-span-1"),
                class_name="grid grid-cols-1 lg:grid-cols-2 gap-6",
            ),
            class_name="w-full max-w-7xl mx-auto",
        ),
        class_name="min-h-screen bg-gray-50 dark:bg-gray-950 p-6 md:p-8 font-['Montserrat'] transition-colors duration-300",
    )