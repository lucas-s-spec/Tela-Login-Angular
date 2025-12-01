import os
import sys
import logging
from supabase import create_client, Client


def setup_admin():
    """
    Script para configurar o usuário administrador no Supabase.
    Versão atualizada com melhor tratamento de erros para Email não confirmado.
    """
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        print("""
❌ ERRO: Variáveis de ambiente não encontradas.

Certifique-se de que as seguintes variáveis estão definidas:
- SUPABASE_URL: URL do seu projeto Supabase
- SUPABASE_KEY: Chave de API (anon/public) do seu projeto
        """)
        return False
    print(f"🔗 Conectando ao Supabase: {url[:30]}...")
    try:
        supabase: Client = create_client(url, key)
        print("✅ Conexão estabelecida com sucesso!")
    except Exception as e:
        logging.exception(f"Erro na conexão: {e}")
        print(f"❌ Erro na conexão: {e}")
        return False
    admin_email = "admin@exemplo.com"
    admin_password = "Admin123!"
    admin_nome = "Administrador do Sistema"
    print(f"\n👤 Configurando usuário administrador...")
    print(f"   Email: {admin_email}")
    user = None
    user_id = None
    print("""
🔍 Tentando autenticar usuário existente...""")
    try:
        session = supabase.auth.sign_in_with_password(
            {"email": admin_email, "password": admin_password}
        )
        if session.user:
            user = session.user
            user_id = user.id
            print("✅ Usuário autenticado com sucesso!")
    except Exception as login_error:
        logging.exception(
            f"Login attempt failed (expected if user does not exist): {login_error}"
        )
        error_msg = str(login_error)
        if "email not confirmed" in error_msg.lower():
            project_ref = "_"
            if "supabase.co" in url:
                try:
                    project_ref = url.split("//")[1].split(".")[0]
                except Exception as e:
                    logging.exception(f"Error extracting project ref: {e}")
            dashboard_link = (
                f"https://supabase.com/dashboard/project/{project_ref}/auth/providers"
            )
            print(
                """
"""
                + "█" * 80
            )
            print(
                "█  🛑 ERRO CRÍTICO DE CONFIGURAÇÃO DO SUPABASE (EMAIL NOT CONFIRMED)          █"
            )
            print(
                "█" * 80
                + """
"""
            )
            print(
                " O Login falhou porque o Supabase está esperando que você clique num link de e-mail."
            )
            print(
                " Como você está em localhost, esse e-mail NUNCA chegará e a conta fica travada."
            )
            print("""
    🛠️  COMO CORRIGIR EM 30 SEGUNDOS:
""")
            print(f"    🔗 1. CLIQUE AQUI: {dashboard_link}")
            print("    👉 2. Clique na seção 'Email' para expandir as configurações.")
            print("    👉 3. DESMARQUE a primeira opção: 'Confirm email'.")
            print("    👉 4. Clique em 'Save' no canto inferior direito.")
            print("""
    🗑️  DEPOIS DE SALVAR (LIMPEZA NECESSÁRIA):
""")
            print("    👉 1. Vá no menu 'Authentication' -> 'Users' no Supabase.")
            print(
                "    👉 2. Delete o usuário 'admin@exemplo.com' (que está com status 'Waiting for verification')."
            )
            print("    👉 3. Rode este script novamente: python app/setup_admin.py")
            print(
                """
"""
                + "█" * 80
                + """
"""
            )
            return False
        elif "Invalid login credentials" in error_msg:
            print("ℹ️  Usuário não encontrado ou senha incorreta. Tentando criar...")
        else:
            print(f"⚠️  Erro no login: {login_error}")
    if not user:
        try:
            print("🆕 Criando novo usuário...")
            auth_response = supabase.auth.sign_up(
                {
                    "email": admin_email,
                    "password": admin_password,
                    "options": {"data": {"nome": admin_nome}},
                }
            )
            if auth_response.user:
                user = auth_response.user
                user_id = user.id
                print(f"✅ Usuário criado com ID: {user_id}")
                if auth_response.session is None:
                    print("""
⚠️  ATENÇÃO: Usuário criado mas sem sessão ativa.""")
                    print("   Provavelmente 'Confirm email' está ativado no Supabase.")
                    print(
                        "   O script tentará prosseguir, mas pode falhar se não tiver permissão pública."
                    )
            else:
                print("❌ Falha ao criar usuário.")
                return False
        except Exception as signup_error:
            logging.exception(f"Error creating user: {signup_error}")
            print(f"❌ Erro ao criar usuário: {signup_error}")
            return False
    if not user_id:
        print("❌ Não foi possível obter o ID do usuário. Abortando.")
        return False
    print(f"\n📋 Gerenciando permissões na tabela 'profiles' para ID: {user_id}...")
    try:
        if supabase.auth.get_session():
            print("🔑 Usando sessão autenticada para atualizar perfil...")
        else:
            print(
                "⚠️  Sem sessão ativa. A atualização do perfil pode falhar devido ao RLS."
            )
        data = {"user_id": user_id, "nome": admin_nome, "role": "admin"}
        upsert_response = supabase.table("profiles").upsert(data).execute()
        if upsert_response.data:
            print("✅ Perfil atualizado/criado com sucesso!")
            print(f"   Role definida como: {upsert_response.data[0].get('role')}")
        else:
            print(
                "✅ Comando enviado. Verifique no dashboard se a role 'admin' foi aplicada."
            )
    except Exception as profile_error:
        logging.exception(f"Erro no perfil: {profile_error}")
        print(f"\n❌ Erro ao atualizar perfil: {profile_error}")
        print(
            """
"""
            + "=" * 60
        )
        print("🛑 AVISO CRÍTICO: ERRO NAS POLÍTICAS DO BANCO DE DADOS")
        print("=" * 60)
        print(
            "Parece que você está enfrentando problemas de permissão ou recursão RLS."
        )
        print("Para corrigir isso IMEDIATAMENTE:")
        print("1. Abra o arquivo 'app/supabase_full_schema.sql' deste projeto.")
        print("2. Copie TODO o conteúdo.")
        print("3. Vá no painel do Supabase -> SQL Editor.")
        print("4. Cole e clique em RUN.")
        print(
            "=" * 60
            + """
"""
        )
        return False
    print(f"\n🎉 Configuração finalizada!")
    print(f"   Login: {admin_email}")
    print(f"   Senha: {admin_password}")
    return True


if __name__ == "__main__":
    setup_admin()