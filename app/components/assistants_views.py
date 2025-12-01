import reflex as rx
from app.states.app_state import AppState
from app.states.assistants_state import AssistantsState
from app.states.assistant_form_state import AssistantFormState
from app.components.auth_views import form_field


def delete_confirmation_modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                "Confirmar Exclusão",
                class_name="text-xl font-bold text-gray-900 dark:text-white mb-4",
            ),
            rx.dialog.description(
                rx.el.div(
                    "Tem certeza que deseja excluir a assistente ",
                    rx.el.span(
                        AssistantsState.assistant_to_delete["name"],
                        class_name="font-semibold",
                    ),
                    "?",
                    rx.el.br(),
                    "Esta ação removerá o assistente da OpenAI e todos os registros associados no banco de dados. ",
                    rx.el.strong("Esta ação não pode ser desfeita."),
                    class_name="text-gray-600 dark:text-gray-300 mt-2",
                )
            ),
            rx.el.div(
                rx.el.button(
                    "Cancelar",
                    on_click=AssistantsState.close_delete_modal,
                    class_name="px-4 py-2 text-gray-700 dark:text-gray-200 bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-lg transition-colors",
                ),
                rx.el.button(
                    rx.cond(
                        AssistantsState.is_deleting,
                        rx.el.span("Excluindo...", class_name="animate-pulse"),
                        "Excluir Permanentemente",
                    ),
                    on_click=AssistantsState.confirm_delete,
                    disabled=AssistantsState.is_deleting,
                    class_name="px-4 py-2 text-white bg-red-600 hover:bg-red-700 rounded-lg transition-colors flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed",
                ),
                class_name="flex justify-end gap-3 mt-6",
            ),
            class_name="bg-white dark:bg-gray-900 p-6 rounded-2xl shadow-2xl border border-gray-100 dark:border-gray-800 max-w-md w-full fixed top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%] z-[60]",
        ),
        open=AssistantsState.is_delete_modal_open,
    )


def sort_header(label: str, field: str) -> rx.Component:
    return rx.el.th(
        rx.el.button(
            label,
            rx.cond(
                AssistantsState.sort_field == field,
                rx.cond(
                    AssistantsState.sort_direction == "asc",
                    rx.icon("arrow-up", class_name="w-3 h-3 ml-1"),
                    rx.icon("arrow-down", class_name="w-3 h-3 ml-1"),
                ),
                rx.icon("arrow-up-down", class_name="w-3 h-3 ml-1 opacity-30"),
            ),
            on_click=AssistantsState.set_sort(field),
            class_name="flex items-center uppercase tracking-wider hover:text-gray-700 dark:hover:text-gray-200 transition-colors",
        ),
        class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 cursor-pointer",
    )


def assistant_row(assistant: dict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    assistant["name"],
                    class_name="font-medium text-gray-900 dark:text-white",
                ),
                rx.el.div(
                    assistant["id"], class_name="text-xs text-gray-400 font-mono mt-0.5"
                ),
                class_name="flex flex-col",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                assistant["model"],
                class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-50 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.span(
                    f"{assistant['credit_used_tokens']}",
                    class_name="text-gray-900 dark:text-white font-medium",
                ),
                rx.el.span(
                    " / ",
                    rx.cond(
                        assistant["credit_limit_tokens"].to(int) > 0,
                        f"{assistant['credit_limit_tokens']}",
                        "∞",
                    ),
                    class_name="text-gray-400 mx-1",
                ),
                class_name="text-sm",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                assistant["created_at"].to_string()[:10],
                class_name="text-sm text-gray-500 dark:text-gray-400",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.a(
                    rx.icon(
                        "layout-dashboard",
                        class_name="w-4 h-4 text-gray-400 hover:text-indigo-600 transition-colors",
                    ),
                    href=f"/dashboard?assistant_id={assistant['id']}",
                    title="Ver no Dashboard",
                    class_name="p-2 hover:bg-indigo-50 dark:hover:bg-indigo-900/20 rounded-lg",
                ),
                rx.el.a(
                    rx.icon(
                        "pencil",
                        class_name="w-4 h-4 text-gray-400 hover:text-blue-600 transition-colors",
                    ),
                    href=f"/assistentes/{assistant['id']}",
                    title="Editar",
                    class_name="p-2 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded-lg",
                ),
                rx.el.button(
                    rx.icon(
                        "trash-2",
                        class_name="w-4 h-4 text-gray-400 hover:text-red-600 transition-colors",
                    ),
                    on_click=AssistantsState.open_delete_modal(assistant),
                    title="Excluir",
                    class_name="p-2 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg",
                ),
                class_name="flex items-center gap-1",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right",
        ),
        class_name="border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors",
    )


def assistants_table() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        sort_header("Nome", "name"),
                        sort_header("Modelo", "model"),
                        rx.el.th(
                            "Uso de Tokens",
                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        sort_header("Criado em", "created_at"),
                        rx.el.th(
                            "Ações",
                            class_name="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                    ),
                    class_name="bg-gray-50 dark:bg-gray-800",
                ),
                rx.el.tbody(
                    rx.foreach(AssistantsState.assistants, assistant_row),
                    class_name="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-800",
                ),
                class_name="min-w-full divide-y divide-gray-200 dark:divide-gray-800",
            ),
            class_name="overflow-x-auto",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Mostrando ",
                    rx.el.span(
                        AssistantsState.page_start,
                        class_name="font-medium text-gray-900 dark:text-white",
                    ),
                    " a ",
                    rx.el.span(
                        AssistantsState.page_end,
                        class_name="font-medium text-gray-900 dark:text-white",
                    ),
                    " de ",
                    rx.el.span(
                        AssistantsState.total_items,
                        class_name="font-medium text-gray-900 dark:text-white",
                    ),
                    " resultados",
                    class_name="text-sm text-gray-700 dark:text-gray-300",
                ),
                class_name="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.button(
                        "Anterior",
                        on_click=AssistantsState.prev_page,
                        disabled=AssistantsState.current_page == 1,
                        class_name="relative inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-700 text-sm font-medium rounded-md text-gray-700 dark:text-gray-200 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed",
                    ),
                    rx.el.button(
                        "Próxima",
                        on_click=AssistantsState.next_page,
                        disabled=AssistantsState.current_page
                        >= AssistantsState.total_pages,
                        class_name="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-700 text-sm font-medium rounded-md text-gray-700 dark:text-gray-200 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed",
                    ),
                    class_name="flex-1 flex justify-between sm:justify-end",
                )
            ),
            class_name="bg-white dark:bg-gray-900 px-4 py-3 border-t border-gray-200 dark:border-gray-800 sm:px-6",
        ),
        class_name="bg-white dark:bg-gray-900 rounded-3xl shadow-sm border border-gray-100 dark:border-gray-800 overflow-hidden",
    )


def assistants_list_view() -> rx.Component:
    return rx.el.div(
        delete_confirmation_modal(),
        rx.el.div(
            rx.el.h1(
                "Assistentes de IA",
                class_name="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white",
            ),
            rx.el.a(
                rx.icon("plus", class_name="w-5 h-5 mr-2"),
                "Nova Assistente",
                href="/assistentes/novo",
                class_name="inline-flex items-center px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium rounded-xl transition-colors shadow-lg shadow-indigo-500/30",
            ),
            class_name="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "search",
                    class_name="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5",
                ),
                rx.el.input(
                    placeholder="Buscar por nome ou modelo...",
                    on_change=AssistantsState.set_search.debounce(300),
                    class_name="w-full pl-10 pr-4 py-2.5 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 outline-none transition-all text-sm",
                ),
                class_name="relative w-full sm:w-72",
            ),
            class_name="mb-6",
        ),
        rx.cond(
            AssistantsState.is_loading,
            rx.el.div(
                rx.el.div(
                    class_name="h-16 bg-gray-100 dark:bg-gray-800 rounded-t-3xl w-full animate-pulse"
                ),
                rx.el.div(
                    class_name="h-64 bg-gray-50 dark:bg-gray-900 w-full animate-pulse border-x border-gray-100 dark:border-gray-800"
                ),
                rx.el.div(
                    class_name="h-12 bg-gray-100 dark:bg-gray-800 rounded-b-3xl w-full animate-pulse"
                ),
                class_name="w-full",
            ),
            rx.cond(
                AssistantsState.total_items > 0,
                assistants_table(),
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "bot",
                            class_name="w-12 h-12 text-gray-300 dark:text-gray-600 mb-4",
                        ),
                        rx.el.h3(
                            "Nenhum assistente encontrado",
                            class_name="text-lg font-medium text-gray-900 dark:text-white",
                        ),
                        rx.el.p(
                            "Tente ajustar sua busca ou crie uma nova assistente.",
                            class_name="text-gray-500 dark:text-gray-400 mt-1",
                        ),
                        class_name="flex flex-col items-center justify-center py-12",
                    ),
                    class_name="bg-white dark:bg-gray-900 rounded-3xl shadow-sm border border-gray-100 dark:border-gray-800 p-8",
                ),
            ),
        ),
        class_name="w-full animate-fade-in",
    )


def assistant_form_layout(is_edit: bool = False) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                form_field(
                    "Nome do Assistente",
                    "Ex: Suporte Técnico",
                    "text",
                    "bot",
                    AssistantFormState.name,
                    AssistantFormState.set_name,
                ),
                rx.el.div(
                    rx.el.label(
                        "Instruções (System Prompt)",
                        class_name="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2",
                    ),
                    rx.el.textarea(
                        placeholder="Descreva como o assistente deve se comportar...",
                        on_change=AssistantFormState.set_instructions,
                        class_name="w-full px-4 py-3 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl focus:border-indigo-500 dark:focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 dark:focus:ring-indigo-900 outline-none transition-all duration-200 text-gray-800 dark:text-white placeholder-gray-400 text-sm font-medium min-h-[200px] resize-none",
                        default_value=AssistantFormState.instructions,
                    ),
                    class_name="mb-5",
                ),
                rx.el.div(
                    rx.el.label(
                        "Modelo OpenAI",
                        class_name="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2",
                    ),
                    rx.el.div(
                        rx.icon(
                            "cpu",
                            class_name="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5",
                        ),
                        rx.el.select(
                            rx.foreach(
                                AssistantFormState.models_list,
                                lambda m: rx.el.option(m, value=m),
                            ),
                            value=AssistantFormState.model,
                            on_change=AssistantFormState.set_model,
                            class_name="w-full pl-10 pr-4 py-3 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl focus:border-indigo-500 dark:focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 dark:focus:ring-indigo-900 outline-none transition-all duration-200 text-gray-800 dark:text-white text-sm font-medium appearance-none cursor-pointer",
                        ),
                        rx.icon(
                            "chevron-down",
                            class_name="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4 pointer-events-none",
                        ),
                        class_name="relative",
                    ),
                    class_name="mb-5",
                ),
                form_field(
                    "Limite de Crédito (Tokens)",
                    "0 para ilimitado",
                    "text",
                    "coins",
                    AssistantFormState.credit_limit,
                    AssistantFormState.set_credit_limit,
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "API Key Override (Opcional)",
                            class_name="block text-sm font-medium text-gray-700 dark:text-gray-300",
                        ),
                        rx.el.span(
                            "Deixe vazio para usar a chave padrão da organização",
                            class_name="text-xs text-gray-500 dark:text-gray-400 ml-2",
                        ),
                        class_name="flex items-baseline mb-2",
                    ),
                    rx.el.div(
                        rx.icon(
                            "key",
                            class_name="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5",
                        ),
                        rx.el.input(
                            type="password",
                            placeholder="sk-...",
                            on_change=AssistantFormState.set_api_key_override,
                            class_name="w-full pl-10 pr-4 py-3 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl focus:border-indigo-500 dark:focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 dark:focus:ring-indigo-900 outline-none transition-all duration-200 text-gray-800 dark:text-white placeholder-gray-400 text-sm font-medium",
                            default_value=AssistantFormState.api_key_override,
                        ),
                        class_name="relative",
                    ),
                    class_name="mb-8",
                ),
                rx.el.button(
                    rx.cond(
                        AssistantFormState.is_saving,
                        rx.el.div(
                            rx.el.div(
                                class_name="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin mr-2"
                            ),
                            "Salvando...",
                            class_name="flex items-center justify-center",
                        ),
                        rx.cond(is_edit, "Salvar Alterações", "Criar Assistente"),
                    ),
                    on_click=AssistantFormState.save,
                    disabled=AssistantFormState.is_saving,
                    class_name="w-full py-3.5 px-4 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl font-semibold transition-all duration-200 shadow-lg hover:shadow-indigo-500/30 disabled:opacity-70 disabled:cursor-not-allowed",
                ),
                class_name="p-6 bg-white dark:bg-gray-900 rounded-3xl border border-gray-100 dark:border-gray-800 shadow-sm",
            ),
            class_name="w-full lg:w-1/2",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "message-square", class_name="w-8 h-8 text-indigo-500 mb-4"
                    ),
                    rx.el.h3(
                        "Chat Playground",
                        class_name="text-lg font-semibold text-gray-900 dark:text-white mb-2",
                    ),
                    rx.el.p(
                        "O ambiente de teste do chat estará disponível aqui após salvar o assistente.",
                        class_name="text-gray-500 dark:text-gray-400 text-center max-w-xs",
                    ),
                    class_name="flex flex-col items-center justify-center h-64",
                ),
                class_name="p-6 bg-gray-50 dark:bg-gray-800/50 rounded-3xl border border-gray-200 dark:border-gray-700 border-dashed h-full min-h-[400px]",
            ),
            class_name="w-full lg:w-1/2",
        ),
        class_name="flex flex-col lg:flex-row gap-6",
    )


def assistant_create_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.a(
                rx.icon("arrow-left", class_name="w-4 h-4 mr-2"),
                "Voltar",
                href="/assistentes",
                class_name="inline-flex items-center text-gray-500 hover:text-indigo-600 dark:text-gray-400 dark:hover:text-indigo-400 transition-colors mb-6",
            ),
            rx.el.h1(
                "Nova Assistente",
                class_name="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white mb-2",
            ),
            rx.el.p(
                f"Criando para: {AppState.selected_org_name}",
                class_name="text-gray-500 dark:text-gray-400",
            ),
            class_name="mb-8",
        ),
        assistant_form_layout(is_edit=False),
        class_name="w-full animate-fade-in",
    )


def assistant_edit_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.a(
                rx.icon("arrow-left", class_name="w-4 h-4 mr-2"),
                "Voltar",
                href="/assistentes",
                class_name="inline-flex items-center text-gray-500 hover:text-indigo-600 dark:text-gray-400 dark:hover:text-indigo-400 transition-colors mb-6",
            ),
            rx.el.h1(
                "Editar Assistente / Chat",
                class_name="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white mb-2",
            ),
            rx.el.p(
                f"Organização: {AppState.selected_org_name}",
                class_name="text-gray-500 dark:text-gray-400",
            ),
            class_name="mb-8",
        ),
        rx.cond(
            AssistantFormState.is_loading,
            rx.el.div(
                rx.el.div(
                    class_name="w-12 h-12 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"
                ),
                class_name="flex justify-center items-center h-64",
            ),
            assistant_form_layout(is_edit=True),
        ),
        class_name="w-full animate-fade-in",
    )