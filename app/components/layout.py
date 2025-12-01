import reflex as rx
from app.states.app_state import AppState
from app.states.auth_state import AuthState
from app.components.auth_views import theme_toggle


def sidebar_item(label: str, icon: str, href: str) -> rx.Component:
    return rx.el.a(
        rx.icon(icon, class_name="w-6 h-6 min-w-[24px]"),
        rx.el.span(
            label,
            class_name="ml-3 font-medium opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap overflow-hidden",
        ),
        href=href,
        class_name="flex items-center p-3 text-gray-700 dark:text-gray-200 hover:bg-indigo-50 dark:hover:bg-gray-800 rounded-xl transition-colors mb-2 group-hover:w-full w-fit",
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "bot",
                    class_name="w-8 h-8 text-indigo-600 dark:text-indigo-400 flex-shrink-0",
                ),
                rx.el.span(
                    "Admin Portal",
                    class_name="ml-3 font-bold text-xl text-gray-900 dark:text-white opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap",
                ),
                class_name="flex items-center h-16 px-3 mb-6",
            ),
            rx.el.nav(
                sidebar_item("Dashboard", "layout-dashboard", "/dashboard"),
                sidebar_item("Assistentes de IA", "sparkles", "/assistentes"),
                class_name="flex flex-col px-2",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("log-out", class_name="w-6 h-6 min-w-[24px]"),
                    rx.el.span(
                        "Sair",
                        class_name="ml-3 font-medium opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap",
                    ),
                    on_click=AuthState.logout,
                    class_name="flex items-center w-full p-3 text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-xl transition-colors",
                ),
                class_name="mt-auto px-2 pb-6",
            ),
            class_name="flex flex-col h-full overflow-hidden",
        ),
        class_name="group fixed left-0 top-0 h-full bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800 shadow-xl z-50 transition-all duration-300 ease-in-out w-20 hover:w-64",
    )


def top_bar() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Organização:",
                    class_name="text-sm font-medium text-gray-500 dark:text-gray-400 mr-3 hidden sm:block",
                ),
                rx.el.div(
                    rx.el.select(
                        rx.foreach(
                            AppState.organizations,
                            lambda org: rx.el.option(org["name"], value=org["id"]),
                        ),
                        value=AppState.selected_org_id,
                        on_change=AppState.set_organization,
                        class_name="bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white text-sm rounded-lg focus:ring-indigo-500 focus:border-indigo-500 block w-full p-2.5 min-w-[200px]",
                    ),
                    rx.cond(
                        AppState.organizations.length() == 0,
                        rx.el.p(
                            "Nenhuma organização encontrada",
                            class_name="text-xs text-red-500 mt-1",
                        ),
                    ),
                ),
                class_name="flex items-center",
            ),
            theme_toggle(),
            class_name="flex items-center justify-between w-full px-6 py-4 bg-white/80 dark:bg-gray-900/80 backdrop-blur-md sticky top-0 z-40 border-b border-gray-100 dark:border-gray-800",
        )
    )


def layout(content: rx.Component) -> rx.Component:
    """
    Wrapper principal de layout da aplicação.
    """
    return rx.el.div(
        sidebar(),
        rx.el.div(
            top_bar(),
            rx.el.main(
                content, class_name="p-6 md:p-8 max-w-7xl mx-auto w-full fade-in"
            ),
            class_name="flex-1 ml-20 transition-all duration-300 min-h-screen bg-gray-50 dark:bg-gray-950",
        ),
        class_name="flex font-['Montserrat'] antialiased bg-gray-50 dark:bg-gray-950",
    )