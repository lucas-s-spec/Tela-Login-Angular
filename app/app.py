import reflex as rx
from app.components.auth_views import login_view
from app.components.dashboard_views import dashboard_view
from app.components.access_denied import access_denied_view
from app.states.auth_state import AuthState
from app.states.dashboard_state import DashboardState


def index() -> rx.Component:
    return login_view()


def dashboard() -> rx.Component:
    return dashboard_view()


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
        rx.el.title("Portal de Vendas - Login"),
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
    on_load=[AuthState.check_dashboard_access, DashboardState.load_data],
    title="Dashboard | Portal Admin",
)
app.add_page(access_denied, route="/acesso-negado", title="Acesso Negado")