import reflex as rx
from app.states.auth_state import AuthState


def access_denied_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("shield-alert", class_name="w-24 h-24 text-red-500 mb-6"),
            rx.el.h1(
                "Acesso Negado",
                class_name="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4 text-center",
            ),
            rx.el.p(
                "Você não tem permissão para acessar esta página.",
                class_name="text-lg text-gray-600 dark:text-gray-400 mb-8 text-center",
            ),
            rx.el.button(
                "Voltar ao Login",
                on_click=AuthState.logout,
                class_name="px-6 py-3 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl font-semibold transition-colors shadow-lg",
            ),
            class_name="flex flex-col items-center justify-center p-8 bg-white dark:bg-gray-900 rounded-3xl shadow-2xl max-w-md w-full border border-gray-100 dark:border-gray-800",
        ),
        class_name="min-h-screen w-full flex items-center justify-center bg-gray-50 dark:bg-gray-950 p-4 font-['Montserrat']",
    )