# Portal de Gestão de Assistentes OpenAI - Reflex + Supabase

## Fase 1: Setup - Database Schema + Helpers Supabase + Verificação OpenAI
- [ ] Criar schema SQL completo (assistants, requests, messages)
- [ ] Criar helpers Python para CRUD Supabase (backend-only, usando SUPABASE_SERVICE_KEY)
- [ ] Instalar e configurar OpenAI SDK
- [ ] Testar conexão OpenAI Assistants API e verificar API keys
- [ ] Criar funções auxiliares para interagir com Assistants API

---

## Fase 2: Layout Base com Sidebar Colapsável
- [ ] Criar componente Sidebar com estado de colapso
- [ ] Implementar animação de hover (expandir ao passar mouse)
- [ ] Adicionar ícones e navegação (Dashboard, Assistentes)
- [ ] Criar layout principal com sidebar + conteúdo
- [ ] Implementar rotas base (/dashboard, /assistentes, /assistentes/novo, /assistentes/:id)

---

## Fase 3: Página Dashboard com Métricas e Filtros
- [ ] Criar filtros (período: Hoje/7d/30d, assistente: Todos + lista)
- [ ] Implementar cards de resumo (total assistentes, requisições, tokens, créditos)
- [ ] Criar gráfico de linha/área (requisições ao longo do tempo)
- [ ] Criar gráfico de barras (tokens por assistente)
- [ ] Criar tabela resumo (assistente, reqs, tokens in/out/total, créditos)
- [ ] Implementar lógica de agregação de dados do Supabase

---

## Fase 4: Página Assistentes (Listagem + CRUD)
- [ ] Criar tabela de assistentes com paginação, ordenação e busca
- [ ] Implementar botão "Cadastrar nova assistente"
- [ ] Criar modal de confirmação para exclusão
- [ ] Implementar ação de editar (navegar para /assistentes/:id)
- [ ] Implementar ação de excluir (remover do Supabase + OpenAI)
- [ ] Adicionar botão para filtrar dashboard por assistente

---

## Fase 5: Página Criar/Editar Assistente + Chat Playground
- [ ] Criar layout de duas colunas (formulário esquerda, chat direita)
- [ ] Implementar formulário (nome, system_prompt, modelo, API key, credit_limit)
- [ ] Lógica de criação: chamar OpenAI API → salvar no Supabase
- [ ] Lógica de edição: carregar dados → atualizar Supabase + OpenAI
- [ ] Implementar chat playground (criar/reutilizar thread_id)
- [ ] Enviar mensagens → polling run → mostrar resposta
- [ ] Registrar requests e messages no Supabase
- [ ] Atualizar credit_used_tokens após cada requisição

---

## Fase 6: Verificação UI e Testes Finais
- [ ] Testar fluxo completo de criação de assistente
- [ ] Testar chat com assistente e registro de tokens
- [ ] Verificar dashboard com filtros e gráficos
- [ ] Validar exclusão e edição de assistentes
- [ ] Confirmar responsividade e animações da sidebar