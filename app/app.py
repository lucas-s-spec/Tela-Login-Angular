import reflex as rx
from app.components.auth_views import login_view
from app.components.dashboard_views import dashboard_view
from app.components.access_denied import access_denied_view
from app.components.assistants_views import (
    assistants_list_view,
    assistant_create_view,
    assistant_edit_view,
)
from app.components.layout import layout
from app.states.auth_state import AuthState
from app.states.dashboard_state import DashboardState
from app.states.app_state import AppState


def index() -> rx.Component:
    return login_view()


def dashboard() -> rx.Component:
    return layout(dashboard_view())


def assistants_list() -> rx.Component:
    return layout(assistants_list_view())


def assistant_create() -> rx.Component:
    return layout(assistant_create_view())


def assistant_edit() -> rx.Component:
    return layout(assistant_edit_view())


def access_denied() -> rx.Component:
    return access_denied_view()


app = rx.App(
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap",
            rel="stylesheet",
        ),
        rx.el.title("Portal Admin - Login"),
        rx.el.style("""
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            .animate-fade-in {
                animation: fadeIn 0.5s ease-out forwards;
            }
            """),
    ],
    theme=rx.theme(
        appearance="light", has_background=True, radius="large", accent_color="indigo"
    ),
    stylesheets=[
        "https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css"
    ],
)
app.add_page(
    index,
    route="/",
    on_load=AuthState.check_login_redirect,
    title="Login | Portal Admin",
)
app.add_page(
    dashboard,
    route="/dashboard",
    on_load=[
        AuthState.check_dashboard_access,
        DashboardState.load_data,
        AppState.load_organizations,
    ],
    title="Dashboard | Portal Admin",
)
from app.states.assistants_state import AssistantsState
from app.states.assistant_form_state import AssistantFormState

app.add_page(
    assistants_list,
    route="/assistentes",
    on_load=[
        AuthState.check_dashboard_access,
        AppState.load_organizations,
        AssistantsState.load_assistants,
    ],
    title="Assistentes | Portal Admin",
)
app.add_page(
    assistant_create,
    route="/assistentes/novo",
    on_load=[
        AuthState.check_dashboard_access,
        AppState.load_organizations,
        AssistantFormState.init_create,
    ],
    title="Novo Assistente | Portal Admin",
)
app.add_page(
    assistant_edit,
    route="/assistentes/[assistant_id]",
    on_load=[
        AuthState.check_dashboard_access,
        AppState.load_organizations,
        AssistantFormState.init_edit,
    ],
    title="Editar Assistente | Portal Admin",
)
app.add_page(access_denied, route="/acesso-negado", title="Acesso Negado")