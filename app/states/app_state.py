import reflex as rx
import logging
from typing import Optional
from app.services.db_service import DBService


class AppState(rx.State):
    organizations: list[dict[str, str]] = []
    selected_org_id: str = ""
    selected_org_name: str = "Selecione uma Organização"

    @rx.event
    async def load_organizations(self):
        """
        Carrega a lista de organizações do banco de dados.
        Define a primeira como selecionada se nenhuma estiver selecionada.
        """
        try:
            orgs = DBService.get_all_organizations()
            self.organizations = orgs
            if self.organizations and (not self.selected_org_id):
                first_org = self.organizations[0]
                self.selected_org_id = str(first_org["id"])
                self.selected_org_name = str(first_org["name"])
            elif self.selected_org_id:
                found = next(
                    (
                        o
                        for o in self.organizations
                        if str(o["id"]) == self.selected_org_id
                    ),
                    None,
                )
                if found:
                    self.selected_org_name = str(found["name"])
        except Exception as e:
            logging.exception(f"Erro ao carregar organizações: {e}")

    @rx.event
    def set_organization(self, org_id: str):
        """
        Define a organização selecionada e atualiza o nome exibido.
        """
        self.selected_org_id = org_id
        found = next((o for o in self.organizations if str(o["id"]) == org_id), None)
        if found:
            self.selected_org_name = str(found["name"])