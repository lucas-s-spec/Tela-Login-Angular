
# Portal de Gestão de Assistentes OpenAI - Reflex + Supabase

## Fase 1: Setup - Database Schema + Helpers Supabase + Verificação OpenAI ✅
- [x] Criar schema SQL completo (organizations, assistants, requests, messages)
- [x] Criar helpers Python para CRUD Supabase (backend-only, usando SUPABASE_KEY)
- [x] Instalar e configurar OpenAI SDK
- [x] Testar conexão OpenAI Assistants API e verificar API keys
- [x] Criar funções auxiliares para interagir com Assistants API

---

## Fase 2: Layout Base com Sidebar Colapsável + Seletor de Organização + Estado Global ✅
- [x] Criar componente Sidebar com estado de colapso (ícones apenas quando colapsada)
- [x] Implementar animação de hover para expandir sidebar (mostrar texto)
- [x] Adicionar ícones Lucide e navegação (Dashboard, Assistentes)
- [x] Criar seletor de organização no topo do conteúdo (select dropdown com lista de orgs)
- [x] Implementar estado global para organização selecionada (AppState)
- [x] Criar layout wrapper principal (sidebar + conteúdo) reutilizável
- [x] Configurar rotas: /dashboard, /assistentes, /assistentes/novo, /assistentes/:id
- [x] Atualizar página dashboard existente para usar novo layout

---

## Fase 3: Página Dashboard com Métricas, Filtros e Gráficos Recharts ✅
- [x] Criar filtros de período (Hoje/7 dias/30 dias) e assistente (Todos + lista)
- [x] Implementar cards de resumo (total assistentes, requisições, tokens consumidos, créditos restantes)
- [x] Criar gráfico de linha/área com Recharts (requisições ao longo do tempo)
- [x] Criar gráfico de barras com Recharts (tokens por assistente quando filtro = Todos)
- [x] Criar tabela resumo (assistente, reqs, tokens in/out/total, créditos restantes)
- [x] Implementar lógica de agregação de dados do Supabase com filtros aplicados
- [x] Adicionar loading states e error handling para todas consultas

---

## Fase 4: Página Assistentes - Listagem Completa com CRUD ✅
- [x] Criar tabela de assistentes com paginação, ordenação e busca
- [x] Exibir colunas: Nome, ID OpenAI, Modelo, Créditos restantes, Total requisições, Data criação, Ações
- [x] Implementar botão "Cadastrar nova assistente de IA" navegando para /assistentes/novo
- [x] Adicionar ação de editar (navegar para /assistentes/:id)
- [x] Adicionar ação de excluir com modal de confirmação
- [x] Implementar exclusão no Supabase (assistants + opcional requests/messages)
- [x] Adicionar botão "Ver no Dashboard" que navega para /dashboard com filtro aplicado
- [x] Implementar busca por nome e ordenação por Nome/Data

---

## Fase 5: Página Criar/Editar Assistente - Formulário + Integração OpenAI ✅
- [x] Criar layout de duas colunas (formulário esquerda, placeholder chat direita)
- [x] Implementar formulário completo (nome, system_prompt, modelo, API key override, credit_limit, parâmetros)
- [x] Lógica de CRIAÇÃO: chamar OpenAI API create assistant → salvar no Supabase com assistant.id
- [x] Lógica de EDIÇÃO: carregar dados do Supabase → atualizar Supabase + OpenAI
- [x] Validação de campos e feedback de erros
- [x] Usar credenciais da organização selecionada (ou override da assistente)
- [x] Após salvar, redirecionar para /assistentes/:id ou permanecer na página
- [x] Loading states durante chamadas OpenAI

---

## Fase 6: Chat Playground - Thread Management + Streaming + Registro
- [ ] Implementar UI do chat na coluna direita (lista de mensagens scrollable)
- [ ] Criar input de texto + botão Enviar com estados de loading
- [ ] Diferenciar visualmente mensagens do usuário vs assistente
- [ ] Gerenciar thread_id: criar thread via OpenAI API ou reutilizar thread existente
- [ ] Implementar envio de mensagem: create message → create run → polling até completed
- [ ] Mostrar resposta do assistente no chat após run completion
- [ ] Registrar TODAS mensagens na tabela messages (assistant_id, thread_id, role, content)
- [ ] Registrar requisição na tabela requests (tokens in/out/total, latency, status, error_message)
- [ ] Atualizar credit_used_tokens do assistente após cada requisição
- [ ] Tratar erros da OpenAI e exibir alertas na UI
- [ ] Adicionar timestamps e formatação de mensagens

---

## Fase 7: Verificação UI Final e Testes de Integração
- [ ] Testar fluxo completo: selecionar organização → criar assistente → chat playground
- [ ] Verificar dashboard com filtros e atualização de métricas após chat
- [ ] Validar exclusão e edição de assistentes
- [ ] Testar registro correto de tokens e requests no Supabase
- [ ] Confirmar responsividade e animações da sidebar
- [ ] Verificar todos os loading states e error handling
