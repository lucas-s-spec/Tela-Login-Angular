import os
import logging
from typing import Optional
from openai import OpenAI


class OpenAIService:
    """
    Serviço para interagir com a OpenAI Assistants API.
    """

    @staticmethod
    def get_client(
        api_key: str, org_id: Optional[str] = None, project_id: Optional[str] = None
    ) -> OpenAI:
        """
        Instancia um cliente OpenAI com as credenciais fornecidas.
        """
        return OpenAI(api_key=api_key, organization=org_id, project=project_id)

    @classmethod
    def create_assistant(
        cls,
        api_key: str,
        name: str,
        instructions: str,
        model: str,
        org_id: Optional[str] = None,
        project_id: Optional[str] = None,
    ) -> dict[str, object]:
        """
        Cria um novo assistente na OpenAI.
        """
        client = cls.get_client(api_key, org_id, project_id)
        try:
            assistant = client.beta.assistants.create(
                name=name, instructions=instructions, model=model
            )
            return assistant.model_dump()
        except Exception as e:
            logging.exception(f"Erro ao criar assistente na OpenAI: {e}")
            raise e

    @classmethod
    def update_assistant(
        cls,
        api_key: str,
        assistant_id: str,
        name: Optional[str] = None,
        instructions: Optional[str] = None,
        model: Optional[str] = None,
        org_id: Optional[str] = None,
        project_id: Optional[str] = None,
    ) -> dict[str, object]:
        """
        Atualiza um assistente existente na OpenAI.
        """
        client = cls.get_client(api_key, org_id, project_id)
        try:
            kwargs = {}
            if name:
                kwargs["name"] = name
            if instructions:
                kwargs["instructions"] = instructions
            if model:
                kwargs["model"] = model
            assistant = client.beta.assistants.update(assistant_id, **kwargs)
            return assistant.model_dump()
        except Exception as e:
            logging.exception(f"Erro ao atualizar assistente {assistant_id}: {e}")
            raise e

    @classmethod
    def delete_assistant(
        cls,
        api_key: str,
        assistant_id: str,
        org_id: Optional[str] = None,
        project_id: Optional[str] = None,
    ) -> bool:
        """
        Remove um assistente da OpenAI.
        """
        client = cls.get_client(api_key, org_id, project_id)
        try:
            response = client.beta.assistants.delete(assistant_id)
            return response.deleted
        except Exception as e:
            logging.exception(f"Erro ao deletar assistente {assistant_id}: {e}")
            raise e

    @classmethod
    def create_thread(
        cls,
        api_key: str,
        org_id: Optional[str] = None,
        project_id: Optional[str] = None,
    ) -> dict[str, object]:
        """
        Cria um novo thread de conversa.
        """
        client = cls.get_client(api_key, org_id, project_id)
        try:
            thread = client.beta.threads.create()
            return thread.model_dump()
        except Exception as e:
            logging.exception(f"Erro ao criar thread: {e}")
            raise e

    @classmethod
    def add_message(
        cls,
        api_key: str,
        thread_id: str,
        content: str,
        role: str = "user",
        org_id: Optional[str] = None,
        project_id: Optional[str] = None,
    ) -> dict[str, object]:
        """
        Adiciona uma mensagem ao thread.
        """
        client = cls.get_client(api_key, org_id, project_id)
        try:
            message = client.beta.threads.messages.create(
                thread_id=thread_id, role=role, content=content
            )
            return message.model_dump()
        except Exception as e:
            logging.exception(f"Erro ao adicionar mensagem ao thread {thread_id}: {e}")
            raise e

    @classmethod
    def create_run(
        cls,
        api_key: str,
        thread_id: str,
        assistant_id: str,
        org_id: Optional[str] = None,
        project_id: Optional[str] = None,
    ) -> dict[str, object]:
        """
        Inicia a execução do assistente no thread.
        """
        client = cls.get_client(api_key, org_id, project_id)
        try:
            run = client.beta.threads.runs.create(
                thread_id=thread_id, assistant_id=assistant_id
            )
            return run.model_dump()
        except Exception as e:
            logging.exception(f"Erro ao criar run para thread {thread_id}: {e}")
            raise e

    @classmethod
    def get_run(
        cls,
        api_key: str,
        thread_id: str,
        run_id: str,
        org_id: Optional[str] = None,
        project_id: Optional[str] = None,
    ) -> dict[str, object]:
        """
        Verifica o status de uma execução.
        """
        client = cls.get_client(api_key, org_id, project_id)
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            return run.model_dump()
        except Exception as e:
            logging.exception(f"Erro ao recuperar run {run_id}: {e}")
            raise e

    @classmethod
    def list_messages(
        cls,
        api_key: str,
        thread_id: str,
        limit: int = 20,
        order: str = "desc",
        org_id: Optional[str] = None,
        project_id: Optional[str] = None,
    ) -> list[dict[str, object]]:
        """
        Lista mensagens de um thread.
        """
        client = cls.get_client(api_key, org_id, project_id)
        try:
            messages = client.beta.threads.messages.list(
                thread_id=thread_id, limit=limit, order=order
            )
            return [msg.model_dump() for msg in messages.data]
        except Exception as e:
            logging.exception(f"Erro ao listar mensagens do thread {thread_id}: {e}")
            raise e