
# 🛑 PARADA OBRIGATÓRIA: LEIA ANTES DE RODAR 🛑

> **⚠️ O LOGIN VAI FALHAR SE VOCÊ NÃO FIZER ISSO AGORA.**
> **Tempo necessário:** 30 segundos.

## 🚨 O Problema: "Email not confirmed"
O Supabase vem configurado para exigir confirmação de e-mail. Como você está rodando em `localhost`, o e-mail nunca chega e **sua conta trava para sempre**.

## ✅ A Solução (Obrigatória)

Você precisa acessar o painel do Supabase e ajustar **DUAS** coisas na seção de Email.

**Onde ir:** `Authentication` > `Providers` > `Email`

### 🖼️ GUIA VISUAL DE CONFIGURAÇÃO

Siga exatamente este padrão:

1. **Enable Email Provider** ➡️ **ON (ATIVADO)** 🟢
   *   *IMPORTANTE: Não desligue o provider! Se desligar, o login deixa de funcionar.* 

2. **Confirm email** ➡️ **OFF (DESMARCADO)** ❌
   *   *CRÍTICO: Desmarque esta caixa para permitir login imediato em localhost.*

text
------------------------------------------------------------------
 Authentication > Providers > Email
------------------------------------------------------------------
 [ / ] Enable Email Provider               <-- TEM QUE ESTAR LIGADO 🟢
------------------------------------------------------------------
 Email Auth configuration

 [ ] Confirm email                         <-- TEM QUE ESTAR DESLIGADO ❌
     (Sends a confirmation email...)

 [ ] Secure password change                <-- Opcional
 ...
------------------------------------------------------------------


**Passo a Passo Final:**
1. Abra seu projeto no Supabase: [Dashboard](https://supabase.com/dashboard/projects)
2. Vá em **Authentication** (ícone de pessoas) > **Providers** > **Email**.
3. **Verifique** se o toggle `Enable Email Provider` está verde (Ligado).
4. **DESMARQUE** a opção `Confirm email` (geralmente a primeira checkbox).
5. Clique em **Save**.
6. *Se já tentou criar o usuário antes, vá em Authentication > Users e delete-o.*

---

# 🚀 Portal Admin com Reflex e Supabase

Este projeto é um painel administrativo moderno construído com **Reflex** (frontend/backend em Python) e **Supabase** (Auth e Banco de Dados).

## 📋 Pré-requisitos

1. **Python 3.11+** instalado.
2. Uma conta no [Supabase](https://supabase.com/).

---

## 🛠️ Configuração do Supabase (Passo a Passo)

Para que o login e o dashboard funcionem, você precisa configurar seu projeto Supabase corretamente.

### 1. Criar Projeto
Crie um novo projeto no painel do Supabase e anote:
- **Project URL**
- **API Key (anon/public)**

### 2. ⚠️ Desabilitar Confirmação de E-mail (CRÍTICO)
**Se você pular esta etapa, o login NÃO funcionará.**

Por padrão, o Supabase exige que novos usuários cliquem num link de e-mail. Em desenvolvimento local (localhost), isso impede o login imediato.

1. Vá no painel do Supabase > **Authentication** (ícone de usuários).
2. No menu lateral, clique em **Providers**.
3. Clique em **Email** para expandir.
4. **DESMARQUE** a opção `Confirm email` (a primeira checkboox).
5. Clique em **Save** no canto inferior direito.

### 3. 🛠️ Corrigir Erro de Banco de Dados (Schema SQL)
Para evitar o erro comum de **"infinite recursion"** nas permissões, você DEVE executar o script SQL incluído.

1. Abra o arquivo `app/supabase_schema.sql` no seu editor de código.
2. Copie **TODO** o conteúdo.
3. Vá no painel do Supabase > **SQL Editor** (ícone de terminal/código).
4. Clique em **New Query**.
5. Cole o código e clique em **Run**.
   - *Isso criará a tabela `profiles` e configurará as políticas de segurança (RLS) corretas.*

---

## 💻 Instalação e Execução Local

### 1. Instalar Dependências
bash
pip install -r requirements.txt


### 2. Configurar Variáveis de Ambiente
No terminal (Linux/Mac):
bash
export SUPABASE_URL="sua-url-do-projeto"
export SUPABASE_KEY="sua-key-anon-public"


No PowerShell (Windows):
powershell
$env:SUPABASE_URL="sua-url-do-projeto"
$env:SUPABASE_KEY="sua-key-anon-public"


### 3. Criar Usuário Administrador
Execute o script automatizado para criar o primeiro admin:

bash
python app/setup_admin.py


- Se tudo der certo, ele exibirá: `✅ Perfil atualizado/criado com sucesso!`
- Credenciais padrão:
  - **Email:** `admin@exemplo.com`
  - **Senha:** `Admin123!`

### 4. Rodar a Aplicação
bash
reflex run

Acesse em: [http://localhost:3000](http://localhost:3000)

---

## 🐛 Solução de Problemas Comuns

### Erro: "Email not confirmed"
- **Causa:** Você pulou o passo 2 da configuração do Supabase.
- **Solução:** Vá em Authentication > Providers > Email e desabilite "Confirm email". Se o usuário já foi criado, delete-o em Authentication > Users e rode o script de setup novamente.

### Erro: "infinite recursion" ou travamento no Dashboard
- **Causa:** Políticas de segurança (RLS) antigas.
- **Solução:** Execute novamente o script SQL `app/supabase_schema.sql` no painel do Supabase. Ele remove as políticas antigas e aplica as versões corrigidas.

### Erro: "Acesso Negado" ao logar
- **Causa:** O usuário existe no Auth, mas não tem a role 'admin' na tabela `profiles`.
- **Solução:** Rode `python app/setup_admin.py` novamente para forçar a atualização da role.

---

## 📁 Estrutura do Projeto

- `app/app.py`: Entrada principal da aplicação e rotas.
- `app/states/`: Lógica de estado (Auth, Dashboard).
- `app/components/`: Componentes UI reutilizáveis.
- `app/services/`: Integração com Supabase.
- `app/supabase_schema.sql`: Definição do banco de dados.
