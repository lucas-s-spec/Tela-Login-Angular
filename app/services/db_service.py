import os
import logging
from typing import Optional
from supabase import create_client, Client


class DBService:
    """
    Serviço para interagir com o banco de dados Supabase.
    Utiliza a Service Key para operações privilegiadas de backend.
    """

    @staticmethod
    def get_client() -> Client:
        """
        Retorna o cliente Supabase com privilégios de serviço (backend).
        """
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_SERVICE_KEY") or os.environ.get("SUPABASE_KEY")
        if not url or not key:
            raise ValueError(
                "SUPABASE_URL e SUPABASE_KEY/SUPABASE_SERVICE_KEY são obrigatórios."
            )
        return create_client(url, key)

    @classmethod
    def get_all_organizations(cls) -> list[dict[str, object]]:
        """
        Retorna todas as organizações cadastradas.
        """
        try:
            response = (
                cls.get_client()
                .table("organizations")
                .select("*")
                .order("name")
                .execute()
            )
            return response.data
        except Exception as e:
            logging.exception(f"Erro ao buscar organizações: {e}")
            return []

    @classmethod
    def get_organization_by_id(cls, org_id: str) -> Optional[dict[str, object]]:
        """
        Retorna uma organização pelo ID.
        """
        try:
            response = (
                cls.get_client()
                .table("organizations")
                .select("*")
                .eq("id", org_id)
                .single()
                .execute()
            )
            return response.data
        except Exception as e:
            logging.exception(f"Erro ao buscar organização {org_id}: {e}")
            return None

    @classmethod
    def create_organization(
        cls, data: dict[str, object]
    ) -> Optional[dict[str, object]]:
        """
        Cria uma nova organização.
        """
        try:
            response = cls.get_client().table("organizations").insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logging.exception(f"Erro ao criar organização: {e}")
            return None

    @classmethod
    def get_assistants_by_organization(cls, org_id: str) -> list[dict[str, object]]:
        """
        Retorna assistentes de uma organização.
        """
        try:
            response = (
                cls.get_client()
                .table("assistants")
                .select("*")
                .eq("organization_id", org_id)
                .order("created_at", desc=True)
                .execute()
            )
            return response.data
        except Exception as e:
            logging.exception(f"Erro ao buscar assistentes da org {org_id}: {e}")
            return []

    @classmethod
    def get_assistant_by_id(cls, assistant_id: str) -> Optional[dict[str, object]]:
        """
        Retorna um assistente pelo ID (que é o ID da OpenAI).
        """
        try:
            response = (
                cls.get_client()
                .table("assistants")
                .select("*")
                .eq("id", assistant_id)
                .single()
                .execute()
            )
            return response.data
        except Exception as e:
            logging.exception(f"Erro ao buscar assistente {assistant_id}: {e}")
            return None

    @classmethod
    def create_assistant(cls, data: dict[str, object]) -> Optional[dict[str, object]]:
        """
        Cria um novo registro de assistente.
        """
        try:
            response = cls.get_client().table("assistants").insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logging.exception(f"Erro ao criar assistente no DB: {e}")
            raise e

    @classmethod
    def update_assistant(
        cls, assistant_id: str, data: dict[str, object]
    ) -> Optional[dict[str, object]]:
        """
        Atualiza um assistente existente.
        """
        try:
            response = (
                cls.get_client()
                .table("assistants")
                .update(data)
                .eq("id", assistant_id)
                .execute()
            )
            return response.data[0] if response.data else None
        except Exception as e:
            logging.exception(f"Erro ao atualizar assistente {assistant_id}: {e}")
            raise e

    @classmethod
    def delete_assistant(cls, assistant_id: str) -> bool:
        """
        Deleta um assistente.
        """
        try:
            response = (
                cls.get_client()
                .table("assistants")
                .delete()
                .eq("id", assistant_id)
                .execute()
            )
            return bool(response.data)
        except Exception as e:
            logging.exception(f"Erro ao deletar assistente {assistant_id}: {e}")
            return False

    @classmethod
    def increment_token_usage(cls, assistant_id: str, tokens: int):
        """
        Incrementa o uso de tokens de um assistente.
        """
        try:
            client = cls.get_client()
            current = (
                client.table("assistants")
                .select("credit_used_tokens")
                .eq("id", assistant_id)
                .single()
                .execute()
            )
            if current.data:
                new_total = (current.data.get("credit_used_tokens") or 0) + tokens
                client.table("assistants").update({"credit_used_tokens": new_total}).eq(
                    "id", assistant_id
                ).execute()
        except Exception as e:
            logging.exception(f"Erro ao incrementar uso de tokens: {e}")

    @classmethod
    def log_request(cls, data: dict[str, object]) -> Optional[dict[str, object]]:
        """
        Registra uma requisição (run/completions).
        """
        try:
            response = cls.get_client().table("requests").insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logging.exception(f"Erro ao logar requisição: {e}")
            return None

    @classmethod
    def log_message(cls, data: dict[str, object]) -> Optional[dict[str, object]]:
        """
        Registra uma mensagem do chat.
        """
        try:
            response = cls.get_client().table("messages").insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logging.exception(f"Erro ao logar mensagem: {e}")
            return None

    @classmethod
    def get_messages_by_thread(cls, thread_id: str) -> list[dict[str, object]]:
        """
        Recupera o histórico de mensagens de um thread.
        """
        try:
            response = (
                cls.get_client()
                .table("messages")
                .select("*")
                .eq("thread_id", thread_id)
                .order("created_at")
                .execute()
            )
            return response.data
        except Exception as e:
            logging.exception(f"Erro ao buscar mensagens do thread {thread_id}: {e}")
            return []

    @classmethod
    def get_dashboard_stats(
        cls, org_id: str, period_days: int = 30, assistant_id: Optional[str] = None
    ) -> dict[str, object]:
        """
        Calcula métricas para o dashboard baseado no schema atualizado.
        """
        try:
            client = cls.get_client()
            assistants = cls.get_assistants_by_organization(org_id)
            assistant_ids = [a["id"] for a in assistants]
            if not assistant_ids:
                return {
                    "total_requests": 0,
                    "total_tokens": 0,
                    "assistants_count": 0,
                    "requests_history": [],
                    "tokens_by_assistant": [],
                    "assistants_data": [],
                }
            req_query = client.table("requests").select("*")
            if assistant_id and assistant_id != "Todos":
                req_query = req_query.eq("assistant_id", assistant_id)
            else:
                req_query = req_query.in_("assistant_id", assistant_ids)
            requests_data = req_query.execute().data
            from datetime import datetime, timedelta

            cutoff_date = datetime.now().astimezone() - timedelta(days=period_days)
            filtered_requests = [
                r
                for r in requests_data
                if datetime.fromisoformat(r["created_at"].replace("Z", "+00:00"))
                >= cutoff_date
            ]
            total_requests = len(filtered_requests)
            total_tokens = sum((r.get("tokens_total", 0) for r in filtered_requests))
            return {
                "total_requests": total_requests,
                "total_tokens": total_tokens,
                "assistants_count": len(assistants),
                "requests_raw": filtered_requests,
                "assistants_data": assistants,
            }
        except Exception as e:
            logging.exception(f"Erro ao calcular estatísticas do dashboard: {e}")
            return {}