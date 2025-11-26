

# 🛠️ Guia de Solução de Problemas (Troubleshooting)

Este guia contém soluções definitivas para os erros de backend (Supabase) mais comuns.

## 🛑 1. ERRO: "Email not confirmed" (O MAIS COMUM)

**Sintoma:**
- Login falha com mensagem: `Email not confirmed` ou `ERRO DE CONFIGURAÇÃO`.
- O script de setup diz "ERRO CRÍTICO".

**A Causa:**
O Supabase exige que novos usuários confirmem o e-mail por padrão. Como você está rodando localmente (`localhost`), não existe servidor de e-mail configurado para enviar esse link, então a conta fica "pendente" para sempre.

**🛠️ Como Resolver (Definitivo):**
1. Acesse o painel do seu projeto no [Supabase](https://supabase.com/dashboard).
2. Navegue até **Authentication** (ícone de duas pessoas no menu lateral).
3. Clique em **Providers** e selecione **Email**.
4. **DESLIGUE** a opção `Confirm email` (a primeira checkbox da lista).
5. Clique em **Save**.
6. Vá na aba **Users** (dentro de Authentication).
7. Se o usuário `admin@exemplo.com` estiver lá, **delete-o** (clique nos `...` > Delete User).
8. Execute `python app/setup_admin.py` novamente.

---

## 🔄 2. Erro Crítico: "infinite recursion" (Recursão Infinita)

**Sintoma:**
- O login funciona, mas o dashboard trava ou não carrega dados.
- Console do navegador mostra erro 500 ou "recursion".
- O script de setup falha ao atualizar o perfil.

**Causa:**
As políticas de segurança (RLS) criaram um loop lógico no banco de dados.

**✅ Solução Definitiva:**
1. Abra o arquivo `app/supabase_schema.sql` deste projeto.
2. Copie TODO o conteúdo.
3. Vá no painel do Supabase -> **SQL Editor** -> **New Query**.
4. Cole o código e clique em **Run**.
5. Isso recria a tabela e aplica políticas corrigidas.

## 3. Erro: Variáveis de Ambiente

**Sintoma:**
`❌ ERRO: Variáveis de ambiente não encontradas.`

**Solução:**
Certifique-se de exportar as variáveis no seu terminal antes de rodar o script ou o app:

bash
# Linux/Mac
export SUPABASE_URL="sua_url_do_projeto"
export SUPABASE_KEY="sua_chave_anon_public"

# Windows (PowerShell)
$env:SUPABASE_URL="sua_url_do_projeto"
$env:SUPABASE_KEY="sua_chave_anon_public"


## 4. Erro: "Failed to fetch user" ou problemas de autenticação

**Sintoma:**
O usuário consegue fazer login, mas não consegue acessar o dashboard ou recebe erros sobre "failed to fetch user".

**Causa:**
Provavelmente as políticas RLS não estão configuradas corretamente ou o perfil do usuário não foi criado.

**Solução:**
1. Execute o SQL Schema completo (`app/supabase_schema.sql`).
2. Execute novamente o `setup_admin.py`.
3. Verifique no painel do Supabase se o perfil foi criado:
   - SQL Editor: `SELECT * FROM public.profiles;`

## 5. Erro: "Permission denied" ao criar perfil

**Sintoma:**
O script `setup_admin.py` cria o usuário mas falha ao criar o perfil na tabela `profiles`.

**Causa:**
As políticas RLS estão muito restritivas ou há problema de permissões.

**Solução:**
1. Execute o SQL Schema completo que recria as políticas.
2. O schema incluirá um trigger automático que cria o perfil quando um usuário é criado.
3. Se o problema persistir, desabilite temporariamente o RLS:
   sql
   ALTER TABLE public.profiles DISABLE ROW LEVEL SECURITY;
   
4. Execute o setup novamente e depois reative:
   sql
   ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
   

## 6. Verificações de Status

Para verificar se tudo está funcionando corretamente, execute estas consultas no SQL Editor:

sql
-- Verificar usuários criados
SELECT id, email, email_confirmed_at, created_at FROM auth.users;

-- Verificar perfis criados  
SELECT user_id, nome, role, created_at FROM public.profiles;

-- Verificar políticas ativas
SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual 
FROM pg_policies 
WHERE tablename = 'profiles';

-- Testar se o RLS está funcionando
SET role anon;
SELECT * FROM public.profiles; -- Deve retornar vazio
RESET role;


## 7. Reset Completo (Última opção)

Se nada funcionar, você pode resetar tudo:

sql
-- CUIDADO: Isso apaga todos os dados!
DROP TABLE IF EXISTS public.profiles CASCADE;
DROP FUNCTION IF EXISTS public.handle_new_user() CASCADE;
DROP FUNCTION IF EXISTS public.handle_updated_at() CASCADE;


Em seguida, execute o `app/supabase_schema.sql` novamente e rode o `setup_admin.py`.

---

## 🎯 Checklist de Configuração Rápida

- [ ] Variáveis de ambiente configuradas (`SUPABASE_URL`, `SUPABASE_KEY`)
- [ ] Confirmação de email desabilitada (Authentication → Providers → Email)
- [ ] SQL Schema executado (`app/supabase_schema.sql`)
- [ ] Script de setup rodado (`python app/setup_admin.py`)
- [ ] Login testado com `admin@exemplo.com` / `Admin123!`

---

*Última atualização: As políticas RLS foram completamente reescritas para evitar recursão infinita, usando apenas `auth.uid()` para verificações de permissão.*

