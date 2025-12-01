import reflex as rx
from datetime import datetime, timedelta
from collections import defaultdict
import logging
from app.services.db_service import DBService


class DashboardState(rx.State):
    total_assistants: int = 0
    total_requests: int = 0
    total_tokens: int = 0
    total_cost_estimated: str = "$ 0.00"
    selected_period: str = "30"
    selected_assistant_id: str = "Todos"
    assistant_options: list[dict[str, str]] = []
    requests_over_time: list[dict[str, str | int]] = []
    tokens_by_assistant: list[dict[str, str | int]] = []
    assistants_summary: list[dict[str, str | int | float]] = []

    @rx.event
    async def load_data(self):
        """
        Carrega dados reais do banco de dados com base nos filtros e organização selecionada.
        """
        from app.states.app_state import AppState

        app_state = await self.get_state(AppState)
        org_id = app_state.selected_org_id
        if not org_id:
            return
        try:
            stats = DBService.get_dashboard_stats(
                org_id=org_id,
                period_days=int(self.selected_period),
                assistant_id=self.selected_assistant_id,
            )
            self.total_assistants = stats.get("assistants_count", 0)
            self.total_requests = stats.get("total_requests", 0)
            self.total_tokens = stats.get("total_tokens", 0)
            cost = self.total_tokens / 1000000 * 0.4
            self.total_cost_estimated = f"$ {cost:.4f}"
            all_assistants = stats.get("assistants_data", [])
            self.assistant_options = [
                {"label": a["name"], "value": a["id"]} for a in all_assistants
            ]
            requests_raw = stats.get("requests_raw", [])
            self._process_timeline_chart(requests_raw)
            self._process_breakdown(requests_raw, all_assistants)
        except Exception as e:
            logging.exception(f"Erro ao carregar dados do dashboard: {e}")

    def _process_timeline_chart(self, requests: list[dict]):
        """Agrupa requisições por dia para o gráfico de área."""
        date_counts = defaultdict(int)
        days = int(self.selected_period)
        base_date = datetime.now()
        for i in range(days):
            d = (base_date - timedelta(days=i)).strftime("%d/%m")
            date_counts[d] = 0
        for req in requests:
            try:
                dt = datetime.fromisoformat(req["created_at"].replace("Z", "+00:00"))
                key = dt.strftime("%d/%m")
                if key in date_counts:
                    date_counts[key] += 1
            except Exception as e:
                logging.exception(f"Erro ao processar data da requisição: {e}")
                continue
        sorted_dates = sorted(
            date_counts.items(),
            key=lambda x: datetime.strptime(
                x[0] + f"/{datetime.now().year}", "%d/%m/%Y"
            ),
        )
        self.requests_over_time = [
            {"date": date, "count": count} for date, count in sorted_dates
        ]

    def _process_breakdown(self, requests: list[dict], assistants: list[dict]):
        """Calcula uso por assistente para gráfico de barras e tabela."""
        usage_by_id = defaultdict(
            lambda: {"reqs": 0, "input": 0, "output": 0, "total": 0}
        )
        for req in requests:
            aid = req.get("assistant_id")
            if aid:
                usage_by_id[aid]["reqs"] += 1
                usage_by_id[aid]["input"] += req.get("tokens_input", 0)
                usage_by_id[aid]["output"] += req.get("tokens_output", 0)
                usage_by_id[aid]["total"] += req.get("tokens_total", 0)
        summary_list = []
        tokens_chart_list = []
        for assistant in assistants:
            aid = assistant["id"]
            name = assistant["name"]
            data = usage_by_id[aid]
            limit = assistant.get("credit_limit_tokens") or 0
            used_global = assistant.get("credit_used_tokens") or 0
            remaining = max(0, limit - used_global) if limit > 0 else "Ilimitado"
            summary_list.append(
                {
                    "name": name,
                    "reqs": data["reqs"],
                    "input": data["input"],
                    "output": data["output"],
                    "total": data["total"],
                    "remaining": str(remaining),
                }
            )
            if data["total"] > 0:
                tokens_chart_list.append({"name": name, "tokens": data["total"]})
        self.assistants_summary = sorted(
            summary_list, key=lambda x: x["total"], reverse=True
        )
        self.tokens_by_assistant = sorted(
            tokens_chart_list, key=lambda x: x["tokens"], reverse=True
        )

    @rx.event
    def set_period(self, period: str):
        self.selected_period = period
        return DashboardState.load_data

    @rx.event
    def set_assistant_filter(self, assistant_id: str):
        self.selected_assistant_id = assistant_id
        return DashboardState.load_data