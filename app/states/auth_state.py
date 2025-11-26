import reflex as rx
import logging
from app.services.supabase_service import SupabaseService


class AuthState(rx.State):
    email: str = ""
    password: str = ""
    remember_me: bool = False
    is_loading: bool = False
    error: str = ""
    access_token: str = rx.Cookie("")
    user: dict[str, str] = {}
    user_profile: dict[str, str | int | bool | None] = {}
    is_authenticated: bool = False
    is_admin: bool = False

    @rx.event
    def set_email(self, value: str):
        self.email = value
        if self.error:
            self.error = ""

    @rx.event
    def set_password(self, value: str):
        self.password = value
        if self.error:
            self.error = ""

    @rx.event
    def toggle_remember_me(self):
        self.remember_me = not self.remember_me

    @rx.event
    async def login(self):
        self.is_loading = True
        self.error = ""
        yield
        if not self.email or not self.password:
            self.error = "Preencha todos os campos."
            self.is_loading = False
            yield
            return
        try:
            response = SupabaseService.login(self.email, self.password)
            if response.user and response.session:
                self.access_token = response.session.access_token
                self.user = {"id": response.user.id, "email": response.user.email}
                self.is_authenticated = True
                user_id = response.user.id
                self.user_profile = SupabaseService.get_user_profile(
                    user_id, self.access_token
                )
                self.is_admin = self.user_profile.get("role") == "admin"
                yield rx.toast("Login realizado com sucesso!", duration=3000)
                yield rx.redirect("/dashboard")
            else:
                self.error = "E-mail ou senha inválidos."
        except Exception as e:
            logging.exception(f"Login Error: {e}")
            error_msg = str(e).lower()
            if "email not confirmed" in error_msg:
                self.error = "ERRO DE CONFIGURAÇÃO: Vá no painel do Supabase > Authentication > Providers > Email e DESMARQUE 'Confirm email'."
            elif "invalid login credentials" in error_msg:
                self.error = "E-mail ou senha inválidos."
            else:
                self.error = "Erro ao fazer login. Tente novamente."
        self.is_loading = False
        yield

    @rx.event
    async def logout(self):
        SupabaseService.logout()
        self.access_token = ""
        self.user = {}
        self.user_profile = {}
        self.is_authenticated = False
        self.is_admin = False
        self.email = ""
        self.password = ""
        yield rx.redirect("/")

    @rx.event
    async def send_password_reset(self):
        if not self.email:
            self.error = "Informe seu e-mail para recuperar a senha."
            return
        try:
            SupabaseService.send_password_reset(self.email)
            yield rx.toast("E-mail de recuperação enviado!", duration=3000)
        except Exception as e:
            logging.exception(f"Error sending password reset: {e}")
            self.error = "Erro ao enviar e-mail. Tente novamente."

    @rx.event
    async def check_login_redirect(self):
        """
        Verifica se o usuário já está logado ao acessar a tela de login.
        Se for admin, redireciona para o dashboard.
        """
        if not self.access_token:
            return
        try:
            user_response = SupabaseService.get_user(self.access_token)
            if user_response and user_response.user:
                user_id = user_response.user.id
                profile = SupabaseService.get_user_profile(user_id, self.access_token)
                if profile.get("role") == "admin":
                    yield rx.redirect("/dashboard")
        except Exception as e:
            logging.exception(f"Session check error on login: {e}")
            self.access_token = ""

    @rx.event
    async def check_dashboard_access(self):
        """
        Protege a rota do dashboard.
        Verifica token, usuário e permissão de admin.
        """
        if not self.access_token:
            yield rx.redirect("/")
            return
        try:
            user_response = SupabaseService.get_user(self.access_token)
            if not user_response or not user_response.user:
                self.access_token = ""
                yield rx.redirect("/")
                return
            self.user = {"id": user_response.user.id, "email": user_response.user.email}
            self.is_authenticated = True
            user_id = user_response.user.id
            self.user_profile = SupabaseService.get_user_profile(
                user_id, self.access_token
            )
            if self.user_profile.get("role") != "admin":
                yield rx.redirect("/acesso-negado")
            else:
                self.is_admin = True
        except Exception as e:
            logging.exception(f"Session check error on dashboard: {e}")
            self.access_token = ""
            yield rx.redirect("/")