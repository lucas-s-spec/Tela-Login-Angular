import reflex as rx
from app.states.auth_state import AuthState


def theme_toggle() -> rx.Component:
    return rx.el.button(
        rx.icon("sun", class_name="w-5 h-5 dark:hidden text-gray-700"),
        rx.icon("moon", class_name="w-5 h-5 hidden dark:block text-gray-200"),
        on_click=rx.toggle_color_mode,
        class_name="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors absolute top-4 right-4 md:top-8 md:right-8 z-50",
    )


def form_field(
    label: str,
    placeholder: str,
    type_: str,
    icon: str,
    value: rx.Var,
    on_change: rx.event.EventType,
) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            label,
            class_name="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2",
        ),
        rx.el.div(
            rx.icon(
                icon,
                class_name="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5",
            ),
            rx.el.input(
                type=type_,
                placeholder=placeholder,
                on_change=on_change,
                class_name="w-full pl-10 pr-4 py-3 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl focus:border-indigo-500 dark:focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 dark:focus:ring-indigo-900 outline-none transition-all duration-200 text-gray-800 dark:text-white placeholder-gray-400 text-sm font-medium",
                default_value=value,
            ),
            class_name="relative",
        ),
        class_name="mb-5",
    )


def login_view() -> rx.Component:
    return rx.el.div(
        theme_toggle(),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "layout-dashboard",
                            class_name="w-10 h-10 text-indigo-600 dark:text-indigo-400",
                        ),
                        class_name="w-16 h-16 bg-indigo-50 dark:bg-indigo-900/30 rounded-2xl flex items-center justify-center mb-6",
                    ),
                    rx.el.h2(
                        "Bem-vindo de volta",
                        class_name="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white mb-2",
                    ),
                    rx.el.p(
                        "Digite suas credenciais para acessar o painel.",
                        class_name="text-gray-500 dark:text-gray-400 text-sm md:text-base mb-8",
                    ),
                    class_name="flex flex-col items-center text-center",
                ),
                rx.el.div(
                    rx.cond(
                        AuthState.error,
                        rx.el.div(
                            rx.icon(
                                "circle-alert", class_name="w-5 h-5 mr-2 flex-shrink-0"
                            ),
                            rx.el.span(AuthState.error),
                            class_name="bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 px-4 py-3 rounded-xl text-sm font-medium flex items-center mb-6 border border-red-100 dark:border-red-800/50 animate-pulse",
                        ),
                    ),
                    form_field(
                        "E-mail",
                        "seu@email.com",
                        "email",
                        "mail",
                        AuthState.email,
                        AuthState.set_email,
                    ),
                    form_field(
                        "Senha",
                        "••••••••",
                        "password",
                        "lock",
                        AuthState.password,
                        AuthState.set_password,
                    ),
                    rx.el.div(
                        rx.el.label(
                            rx.el.input(
                                type="checkbox",
                                checked=AuthState.remember_me,
                                on_change=AuthState.toggle_remember_me,
                                class_name="w-4 h-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500 dark:bg-gray-700 dark:border-gray-600 cursor-pointer",
                            ),
                            rx.el.span(
                                "Lembrar-me",
                                class_name="ml-2 text-sm text-gray-600 dark:text-gray-300",
                            ),
                            class_name="flex items-center cursor-pointer",
                        ),
                        rx.el.button(
                            "Esqueci minha senha",
                            on_click=AuthState.send_password_reset,
                            class_name="text-sm font-medium text-indigo-600 dark:text-indigo-400 hover:text-indigo-700 dark:hover:text-indigo-300 transition-colors",
                        ),
                        class_name="flex items-center justify-between mb-8",
                    ),
                    rx.el.button(
                        rx.cond(
                            AuthState.is_loading,
                            rx.el.div(
                                rx.el.div(
                                    class_name="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin mr-2"
                                ),
                                "Entrando...",
                                class_name="flex items-center justify-center",
                            ),
                            "Entrar",
                        ),
                        on_click=AuthState.login,
                        disabled=AuthState.is_loading,
                        class_name=rx.cond(
                            AuthState.is_loading,
                            "w-full py-3.5 px-4 bg-indigo-400 text-white rounded-xl font-semibold cursor-not-allowed shadow-sm",
                            "w-full py-3.5 px-4 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl font-semibold transition-all duration-200 shadow-lg hover:shadow-indigo-500/30 active:scale-[0.98]",
                        ),
                    ),
                    class_name="w-full",
                ),
                class_name="w-full max-w-[440px] mx-auto p-8 md:p-10 bg-white dark:bg-gray-900 rounded-3xl shadow-xl dark:shadow-2xl border border-gray-100 dark:border-gray-800",
            ),
            rx.el.p(
                "Não tem uma conta? ",
                rx.el.a(
                    "Entre em contato com o administrador.",
                    href="#",
                    class_name="font-semibold text-indigo-600 dark:text-indigo-400 hover:underline transition-colors",
                ),
                class_name="mt-8 text-center text-sm text-gray-500 dark:text-gray-400",
            ),
            class_name="flex flex-col items-center justify-center w-full p-4",
        ),
        class_name="min-h-screen w-full flex items-center justify-center bg-gray-50 dark:bg-gray-950 text-gray-900 dark:text-white transition-colors duration-300 font-['Montserrat']",
    )