import reflex as rx
import logging
import os
from app.services.db_service import DBService
from app.services.openai_service import OpenAIService
from app.states.app_state import AppState


class AssistantFormState(rx.State):
    name: str = ""
    instructions: str = ""
    model: str = "gpt-4o"
    credit_limit: str = "0"
    api_key_override: str = ""
    is_loading: bool = False
    is_saving: bool = False
    current_assistant_id: str = ""
    models_list: list[str] = ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"]

    @rx.event
    def set_name(self, value: str):
        self.name = value

    @rx.event
    def set_instructions(self, value: str):
        self.instructions = value

    @rx.event
    def set_model(self, value: str):
        self.model = value

    @rx.event
    def set_credit_limit(self, value: str):
        if value.isdigit() or value == "":
            self.credit_limit = value

    @rx.event
    def set_api_key_override(self, value: str):
        self.api_key_override = value

    @rx.event
    def init_create(self):
        """Resets form for creation."""
        self.name = ""
        self.instructions = "Você é um assistente útil."
        self.model = "gpt-4o"
        self.credit_limit = "0"
        self.api_key_override = ""
        self.current_assistant_id = ""
        self.is_loading = False
        self.is_saving = False

    @rx.event
    async def init_edit(self):
        """Loads assistant data for editing."""
        self.init_create()
        self.is_loading = True
        yield
        try:
            assistant_id = self.router.page.params.get("assistant_id")
            if not assistant_id:
                yield rx.toast("ID do assistente não encontrado.", duration=3000)
                self.is_loading = False
                yield
                return
            self.current_assistant_id = assistant_id
            data = DBService.get_assistant_by_id(assistant_id)
            if data:
                self.name = str(data.get("name", ""))
                self.instructions = str(data.get("instructions", ""))
                self.model = str(data.get("model", "gpt-4o"))
                self.credit_limit = str(data.get("credit_limit_tokens", 0))
                self.api_key_override = str(data.get("api_key_override", "") or "")
            else:
                yield rx.toast(
                    "Assistente não encontrado no banco de dados.", duration=3000
                )
        except Exception as e:
            logging.exception(f"Error loading assistant for edit: {e}")
            yield rx.toast(f"Erro ao carregar assistente: {e}", duration=3000)
        self.is_loading = False
        yield

    @rx.event
    async def save(self):
        self.is_saving = True
        yield
        if not self.name or not self.instructions:
            yield rx.toast("Nome e Instruções são obrigatórios.", duration=3000)
            self.is_saving = False
            yield
            return
        api_key = self.api_key_override or os.environ.get("OPENAI_API_KEY")
        if not api_key:
            yield rx.toast("API Key da OpenAI não configurada.", duration=3000)
            self.is_saving = False
            yield
            return
        app_state = await self.get_state(AppState)
        org_id = app_state.selected_org_id
        if not org_id and (not self.current_assistant_id):
            yield rx.toast("Selecione uma organização primeiro.", duration=3000)
            self.is_saving = False
            yield
            return
        try:
            credit_limit_int = int(self.credit_limit) if self.credit_limit else 0
            if self.current_assistant_id:
                OpenAIService.update_assistant(
                    api_key=api_key,
                    assistant_id=self.current_assistant_id,
                    name=self.name,
                    instructions=self.instructions,
                    model=self.model,
                )
                db_data = {
                    "name": self.name,
                    "instructions": self.instructions,
                    "model": self.model,
                    "credit_limit_tokens": credit_limit_int,
                    "api_key_override": self.api_key_override
                    if self.api_key_override
                    else None,
                }
                DBService.update_assistant(self.current_assistant_id, db_data)
                yield rx.toast("Assistente atualizado com sucesso!", duration=3000)
            else:
                openai_res = OpenAIService.create_assistant(
                    api_key=api_key,
                    name=self.name,
                    instructions=self.instructions,
                    model=self.model,
                )
                new_id = openai_res.get("id")
                db_data = {
                    "id": new_id,
                    "organization_id": org_id,
                    "name": self.name,
                    "instructions": self.instructions,
                    "model": self.model,
                    "credit_limit_tokens": credit_limit_int,
                    "api_key_override": self.api_key_override
                    if self.api_key_override
                    else None,
                    "credit_used_tokens": 0,
                }
                DBService.create_assistant(db_data)
                yield rx.toast("Assistente criado com sucesso!", duration=3000)
                yield rx.redirect(f"/assistentes/{new_id}")
        except Exception as e:
            logging.exception(f"Error saving assistant: {e}")
            yield rx.toast(f"Erro ao salvar: {e}", duration=5000)
        self.is_saving = False
        yield