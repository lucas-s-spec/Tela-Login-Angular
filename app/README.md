
# 🛑 PARADA OBRIGATÓRIA: LEIA ANTES DE RODAR 🛑

> **⚠️ O LOGIN VAI FALHAR SE VOCÊ NÃO FIZER ISSO AGORA.**
> **Tempo necessário:** 30 segundos.

## 🚨 1. Configuração de Email (Obrigatória)
Você precisa acessar o painel do Supabase e ajustar **DUAS** coisas na seção de Email.

**Onde ir:** `Authentication` > `Providers` > `Email`

1. **Enable Email Provider** ➡️ **ON (ATIVADO)** 🟢
2. **Confirm email** ➡️ **OFF (DESMARCADO)** ❌

---

## 🚨 2. Atualização do Banco de Dados (NOVO)
**Este passo é CRÍTICO para o funcionamento do sistema de Assistentes e Organizações.**

O schema do banco de dados foi atualizado para suportar múltiplas organizações e logs detalhados.

1. Abra o arquivo `app/supabase_full_schema.sql` neste projeto.
2. Copie **TODO** o conteúdo.
3. Vá no painel do Supabase > **SQL Editor** (ícone de terminal/código).
4. Clique em **New Query**.
5. Cole o código e clique em **Run**.

Isso criará as tabelas: `organizations`, `assistants`, `requests`, `messages`.

### ✅ Como verificar se funcionou?
No painel esquerdo do Supabase, clique em **Table Editor** (ícone de tabela). Você deve ver as novas tabelas listadas lá. Se elas aparecerem, seu banco de dados está pronto!

---

## 🚀 Portal Admin com Reflex e Supabase

Este projeto é um painel administrativo moderno construído com **Reflex** (frontend/backend em Python) e **Supabase** (Auth e Banco de Dados).

## 📋 Pré-requisitos

1. **Python 3.11+** instalado.
2. Uma conta no [Supabase](https://supabase.com/).
3. Uma chave de API da **OpenAI**.

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
export SUPABASE_SERVICE_KEY="sua-service-role-key" # Necessário para bypass de RLS
export OPENAI_API_KEY="sk-..."


No PowerShell (Windows):
powershell
$env:SUPABASE_URL="sua-url-do-projeto"
$env:SUPABASE_KEY="sua-key-anon-public"
$env:SUPABASE_SERVICE_KEY="sua-service-role-key"
$env:OPENAI_API_KEY="sk-..."


### 3. Criar Usuário Administrador
Execute o script automatizado para criar o primeiro admin:

bash
python app/setup_admin.py


### 4. Rodar a Aplicação
bash
reflex run

Acesse em: [http://localhost:3000](http://localhost:3000)
