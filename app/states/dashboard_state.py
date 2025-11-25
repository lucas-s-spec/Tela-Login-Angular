import reflex as rx
import random
from datetime import datetime, timedelta


class DashboardState(rx.State):
    total_sales: str = "R$ 0,00"
    total_items: int = 0
    monthly_sales: str = "R$ 0,00"
    avg_ticket: str = "R$ 0,00"
    sales_history: list[dict[str, str | int | float]] = []
    product_performance: list[dict[str, str | int]] = []
    product_share: list[dict[str, str | int]] = []

    @rx.event
    def load_data(self):
        """
        Gera dados mockados realistas para o dashboard.
        Simula um crescimento de vendas ao longo dos meses.
        """
        products = ["COD001", "COD002", "COD003", "COD004"]
        history = []
        current_date = datetime.now()
        total_revenue_acc = 0
        total_qty_acc = 0
        product_counts = {p: 0 for p in products}
        colors = ["#6366f1", "#8b5cf6", "#ec4899", "#10b981"]
        for i in range(5, -1, -1):
            date = current_date - timedelta(days=30 * i)
            month_name = date.strftime("%b")
            growth_factor = 1 + 0.1 * (5 - i)
            month_revenue = 0
            month_data = {"month": month_name}
            for p in products:
                base_qty = random.randint(15, 40)
                qty = int(base_qty * growth_factor)
                price = random.uniform(80.0, 150.0)
                revenue = qty * price
                month_data[p] = qty
                product_counts[p] += qty
                month_revenue += revenue
                total_qty_acc += qty
            month_data["total_revenue"] = round(month_revenue, 2)
            history.append(month_data)
            total_revenue_acc += month_revenue
        self.sales_history = history
        self.total_sales = self._format_currency(total_revenue_acc)
        self.total_items = total_qty_acc
        last_month_rev = history[-1]["total_revenue"]
        self.monthly_sales = self._format_currency(last_month_rev)
        avg = total_revenue_acc / total_qty_acc if total_qty_acc > 0 else 0
        self.avg_ticket = self._format_currency(avg)
        self.product_performance = [
            {"name": p, "value": qty} for p, qty in product_counts.items()
        ]
        self.product_share = [
            {"name": p, "value": qty, "fill": colors[i % len(colors)]}
            for i, (p, qty) in enumerate(product_counts.items())
        ]

    def _format_currency(self, value: float) -> str:
        """Formata float para moeda BRL (gambiarra para locale pt-BR simples)"""
        return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")