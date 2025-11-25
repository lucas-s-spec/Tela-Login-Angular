import os
import logging
from typing import Optional
from supabase import create_client, Client


class SupabaseService:
    """
    Serviço para interagir com o Supabase.
    Gerencia autenticação e consultas ao banco de dados de forma stateless.
    """

    @classmethod
    def get_client(cls) -> Optional[Client]:
        """Retorna uma nova instância do cliente Supabase."""
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        if not url or not key:
            logging.warning(
                "Supabase credentials not found. Please check SUPABASE_URL and SUPABASE_KEY."
            )
            return None
        return create_client(url, key)

    @classmethod
    def login(cls, email: str, password: str):
        """Realiza login e retorna a sessão do usuário."""
        client = cls.get_client()
        if not client:
            raise Exception("Supabase client not initialized")
        return client.auth.sign_in_with_password({"email": email, "password": password})

    @classmethod
    def logout(cls):
        """Realiza logout (opcional, pois o estado é mantido no client-side/Reflex state)."""
        client = cls.get_client()
        if client:
            return client.auth.sign_out()

    @classmethod
    def get_user(cls, access_token: str):
        """Obtém o usuário atual a partir do token de acesso."""
        client = cls.get_client()
        if not client or not access_token:
            return None
        try:
            return client.auth.get_user(access_token)
        except Exception as e:
            logging.exception(f"Error fetching user: {e}")
            return None

    @classmethod
    def get_user_profile(
        cls, user_id: str, access_token: str = None
    ) -> dict[str, str | int | bool | None]:
        """
        Busca o perfil do usuário na tabela 'profiles'.
        Requer access_token para respeitar as políticas RLS.
        """
        client = cls.get_client()
        if not client:
            return {}
        try:
            if access_token:
                client.postgrest.auth(access_token)
            response = (
                client.table("profiles")
                .select("*")
                .eq("user_id", user_id)
                .single()
                .execute()
            )
            return response.data if response.data else {}
        except Exception as e:
            logging.exception(f"Error fetching profile for {user_id}: {e}")
            return {}

    @classmethod
    def send_password_reset(cls, email: str):
        """Envia e-mail de recuperação de senha."""
        client = cls.get_client()
        if not client:
            raise Exception("Supabase client not initialized")
        return client.auth.reset_password_for_email(email)