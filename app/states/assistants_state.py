import reflex as rx
import logging
import os
import math
from typing import Any
from app.services.db_service import DBService
from app.services.openai_service import OpenAIService
from app.states.app_state import AppState


class AssistantsState(rx.State):
    assistants: list[dict[str, str | int | float | bool | None]] = []
    total_items: int = 0
    current_page: int = 1
    items_per_page: int = 10
    total_pages: int = 1
    search_query: str = ""
    sort_field: str = "name"
    sort_direction: str = "asc"
    is_loading: bool = False
    is_delete_modal_open: bool = False
    assistant_to_delete: dict[str, str | int | float | bool | None] = {}
    is_deleting: bool = False

    @rx.var
    def page_start(self) -> int:
        if self.total_items == 0:
            return 0
        return (self.current_page - 1) * self.items_per_page + 1

    @rx.var
    def page_end(self) -> int:
        end = self.current_page * self.items_per_page
        return end if end < self.total_items else self.total_items

    @rx.event
    async def load_assistants(self):
        self.is_loading = True
        yield
        try:
            app_state = await self.get_state(AppState)
            org_id = app_state.selected_org_id
            if not org_id:
                self.assistants = []
                self.total_items = 0
                self.is_loading = False
                yield
                return
            raw_assistants = DBService.get_assistants_by_organization(org_id)
            filtered = []
            query = self.search_query.lower()
            for a in raw_assistants:
                name = str(a.get("name", "")).lower()
                model = str(a.get("model", "")).lower()
                if query in name or query in model:
                    filtered.append(a)
            reverse = self.sort_direction == "desc"
            filtered.sort(
                key=lambda x: str(x.get(self.sort_field) or "").lower(), reverse=reverse
            )
            self.total_items = len(filtered)
            self.total_pages = math.ceil(self.total_items / self.items_per_page)
            if self.total_pages == 0:
                self.total_pages = 1
            if self.current_page > self.total_pages:
                self.current_page = self.total_pages
            start = (self.current_page - 1) * self.items_per_page
            end = start + self.items_per_page
            self.assistants = filtered[start:end]
        except Exception as e:
            logging.exception(f"Error loading assistants: {e}")
            yield rx.toast("Erro ao carregar assistentes.", duration=3000)
        self.is_loading = False
        yield

    @rx.event
    def set_search(self, query: str):
        self.search_query = query
        self.current_page = 1
        return AssistantsState.load_assistants

    @rx.event
    def set_sort(self, field: str):
        if self.sort_field == field:
            self.sort_direction = "desc" if self.sort_direction == "asc" else "asc"
        else:
            self.sort_field = field
            self.sort_direction = "asc"
        return AssistantsState.load_assistants

    @rx.event
    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            return AssistantsState.load_assistants

    @rx.event
    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            return AssistantsState.load_assistants

    @rx.event
    def open_delete_modal(self, assistant: dict[str, Any]):
        self.assistant_to_delete = assistant
        self.is_delete_modal_open = True

    @rx.event
    def close_delete_modal(self):
        self.is_delete_modal_open = False
        self.assistant_to_delete = {}

    @rx.event
    async def confirm_delete(self):
        if not self.assistant_to_delete:
            return
        self.is_deleting = True
        yield
        try:
            assistant_id = self.assistant_to_delete.get("id")
            name = self.assistant_to_delete.get("name", "Assistente")
            api_key = os.environ.get("OPENAI_API_KEY")
            openai_deleted = False
            if api_key:
                try:
                    OpenAIService.delete_assistant(api_key, assistant_id)
                    openai_deleted = True
                except Exception as e:
                    logging.exception(f"Failed to delete from OpenAI: {e}")
                    yield rx.toast(
                        f"Aviso: Não foi possível remover da OpenAI ({str(e)}), removendo do banco local...",
                        duration=5000,
                    )
            success = DBService.delete_assistant(assistant_id)
            if success:
                msg = f"{name} removido com sucesso!"
                if api_key and (not openai_deleted):
                    msg += " (Apenas do banco de dados)"
                yield rx.toast(msg, duration=3000)
                self.is_delete_modal_open = False
                self.assistant_to_delete = {}
                yield AssistantsState.load_assistants
            else:
                yield rx.toast(
                    "Erro ao remover assistente do banco de dados.", duration=4000
                )
        except Exception as e:
            logging.exception(f"Error deleting assistant: {e}")
            yield rx.toast(f"Erro crítico ao excluir: {e}", duration=5000)
        self.is_deleting = False
        yield