import reflex as rx
from app.states.auth_state import AuthState


def social_button(icon: str, text: str) -> rx.Component:
    return rx.el.button(
        rx.icon(icon, class_name="w-5 h-5 mr-2 opacity-70"),
        rx.el.span(text, class_name="text-sm font-medium"),
        class_name="flex items-center justify-center w-full px-4 py-2.5 border border-gray-200 rounded-xl hover:bg-gray-50 hover:border-gray-300 transition-all duration-200 focus:ring-2 focus:ring-indigo-100 focus:outline-none bg-white text-gray-700 shadow-sm hover:shadow-md active:scale-95",
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
            label, class_name="block text-sm font-semibold text-gray-700 mb-1.5"
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
                class_name="w-full pl-10 pr-4 py-2.5 bg-white border border-gray-200 rounded-xl focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition-all duration-200 text-gray-800 placeholder-gray-400 text-sm font-medium",
                default_value=value,
            ),
            class_name="relative",
        ),
        class_name="mb-5",
    )


def login_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("command", class_name="w-8 h-8 text-white mb-2"),
                    rx.el.h2(
                        "Nexus",
                        class_name="text-2xl font-bold text-white tracking-tight",
                    ),
                    class_name="flex items-center gap-3 mb-12",
                ),
                rx.el.div(
                    rx.el.h1(
                        "Turn your ideas into reality.",
                        class_name="text-4xl md:text-5xl font-bold text-white mb-6 leading-tight",
                    ),
                    rx.el.p(
                        "Start building beautiful applications with the power of pure Python. Join thousands of developers creating the future.",
                        class_name="text-indigo-100 text-lg leading-relaxed max-w-md",
                    ),
                    class_name="flex-1 flex flex-col justify-center",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.image(
                                src="https://api.dicebear.com/9.x/avataaars/svg?seed=Felix",
                                class_name="w-10 h-10 rounded-full border-2 border-white",
                            ),
                            rx.image(
                                src="https://api.dicebear.com/9.x/avataaars/svg?seed=Aneka",
                                class_name="w-10 h-10 rounded-full border-2 border-white -ml-3",
                            ),
                            rx.image(
                                src="https://api.dicebear.com/9.x/avataaars/svg?seed=Milo",
                                class_name="w-10 h-10 rounded-full border-2 border-white -ml-3",
                            ),
                            rx.el.div(
                                "2k+",
                                class_name="w-10 h-10 rounded-full border-2 border-white -ml-3 bg-indigo-500 flex items-center justify-center text-xs font-bold text-white",
                            ),
                            class_name="flex items-center mb-4",
                        ),
                        rx.el.div(
                            rx.icon(
                                "star",
                                class_name="w-4 h-4 text-yellow-400 fill-current",
                            ),
                            rx.icon(
                                "star",
                                class_name="w-4 h-4 text-yellow-400 fill-current",
                            ),
                            rx.icon(
                                "star",
                                class_name="w-4 h-4 text-yellow-400 fill-current",
                            ),
                            rx.icon(
                                "star",
                                class_name="w-4 h-4 text-yellow-400 fill-current",
                            ),
                            rx.icon(
                                "star",
                                class_name="w-4 h-4 text-yellow-400 fill-current",
                            ),
                            class_name="flex gap-1 mb-1",
                        ),
                        rx.el.p(
                            "Loved by developers worldwide",
                            class_name="text-sm text-indigo-100 font-medium",
                        ),
                    ),
                    class_name="mt-auto",
                ),
                class_name="h-full flex flex-col p-12 relative z-10",
            ),
            rx.el.div(
                class_name="absolute top-0 right-0 -mr-20 -mt-20 w-96 h-96 bg-white opacity-10 blur-3xl rounded-full"
            ),
            rx.el.div(
                class_name="absolute bottom-0 left-0 -ml-20 -mb-20 w-80 h-80 bg-purple-500 opacity-20 blur-3xl rounded-full"
            ),
            class_name="hidden lg:block w-1/2 bg-gradient-to-br from-indigo-600 to-violet-700 relative overflow-hidden",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "command", class_name="w-8 h-8 text-indigo-600 mb-2 lg:hidden"
                    ),
                    class_name="flex items-center justify-center lg:hidden mb-8",
                ),
                rx.el.div(
                    rx.el.h2(
                        "Welcome back",
                        class_name="text-2xl md:text-3xl font-bold text-gray-900 mb-2",
                    ),
                    rx.el.p(
                        "Please enter your details to sign in.",
                        class_name="text-gray-500 text-sm md:text-base mb-8",
                    ),
                    class_name="text-center lg:text-left",
                ),
                rx.el.div(
                    social_button("github", "GitHub"),
                    social_button("mail", "Google"),
                    class_name="grid grid-cols-2 gap-4 mb-8",
                ),
                rx.el.div(
                    rx.el.div(class_name="flex-grow border-t border-gray-200"),
                    rx.el.span(
                        "or continue with email",
                        class_name="px-4 text-xs text-gray-500 font-medium uppercase tracking-wide bg-white",
                    ),
                    rx.el.div(class_name="flex-grow border-t border-gray-200"),
                    class_name="relative flex items-center justify-center mb-8",
                ),
                rx.el.div(
                    rx.cond(
                        AuthState.error,
                        rx.el.div(
                            rx.icon(
                                "circle-alert", class_name="w-4 h-4 mr-2 flex-shrink-0"
                            ),
                            rx.el.span(AuthState.error),
                            class_name="bg-red-50 text-red-600 px-4 py-3 rounded-xl text-sm font-medium flex items-center mb-6 border border-red-100 animate-pulse",
                        ),
                    ),
                    form_field(
                        "Email",
                        "you@example.com",
                        "email",
                        "mail",
                        AuthState.email,
                        AuthState.set_email,
                    ),
                    form_field(
                        "Password",
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
                                class_name="w-4 h-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500 cursor-pointer",
                            ),
                            rx.el.span(
                                "Remember me", class_name="ml-2 text-sm text-gray-600"
                            ),
                            class_name="flex items-center cursor-pointer",
                        ),
                        rx.el.a(
                            "Forgot password?",
                            href="#",
                            class_name="text-sm font-medium text-indigo-600 hover:text-indigo-700 transition-colors",
                        ),
                        class_name="flex items-center justify-between mb-8",
                    ),
                    rx.el.button(
                        rx.cond(
                            AuthState.is_loading,
                            rx.el.div(
                                rx.el.div(
                                    class_name="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"
                                ),
                                "Signing in...",
                                class_name="flex items-center justify-center",
                            ),
                            "Sign in",
                        ),
                        on_click=AuthState.login,
                        disabled=AuthState.is_loading,
                        class_name=rx.cond(
                            AuthState.is_loading,
                            "w-full py-3 px-4 bg-indigo-400 text-white rounded-xl font-semibold cursor-not-allowed shadow-sm",
                            "w-full py-3 px-4 bg-indigo-600 text-white rounded-xl font-semibold hover:bg-indigo-700 transition-all duration-200 shadow-lg hover:shadow-xl active:scale-[0.98] hover:-translate-y-0.5",
                        ),
                    ),
                    class_name="w-full",
                ),
                rx.el.p(
                    "Don't have an account? ",
                    rx.el.a(
                        "Sign up for free",
                        href="#",
                        class_name="font-semibold text-indigo-600 hover:text-indigo-700 transition-colors",
                    ),
                    class_name="mt-8 text-center text-sm text-gray-600",
                ),
                class_name="w-full max-w-md mx-auto",
            ),
            class_name="w-full lg:w-1/2 flex items-center justify-center p-6 md:p-12 lg:p-24 bg-white",
        ),
        class_name="flex min-h-screen w-full font-['Montserrat'] bg-white",
    )