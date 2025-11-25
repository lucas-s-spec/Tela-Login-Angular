import os
import sys
import logging
from supabase import create_client, Client


def setup_admin():
    """
    Script para configurar o usuário administrador no Supabase.

    Este script:
    1. Conecta ao Supabase usando as credenciais do ambiente
    2. Cria ou verifica o usuário admin@exemplo.com
    3. Garante que o usuário tenha role 'admin' na tabela profiles
    """
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        print("""
❌ ERRO: Variáveis de ambiente não encontradas.

Certifique-se de que as seguintes variáveis estão definidas:
- SUPABASE_URL: URL do seu projeto Supabase
- SUPABASE_KEY: Chave de API (anon/public) do seu projeto

Exemplo de configuração:
export SUPABASE_URL="https://seu-projeto.supabase.co"
export SUPABASE_KEY="sua-chave-publica-aqui"
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
    print(f"   Nome: {admin_nome}")
    user = None
    user_id = None
    try:
        print("""
🔍 Verificando se o usuário já existe...""")
        try:
            session = supabase.auth.sign_in_with_password(
                {"email": admin_email, "password": admin_password}
            )
            user = session.user
            print("✅ Usuário encontrado e senha correta!")
        except Exception as login_error:
            logging.exception(
                f"Usuário não encontrado ou senha incorreta: {login_error}"
            )
            print(
                "👤 Usuário não encontrado ou senha incorreta. Criando novo usuário..."
            )
            try:
                auth_response = supabase.auth.sign_up(
                    {
                        "email": admin_email,
                        "password": admin_password,
                        "options": {"data": {"nome": admin_nome}},
                    }
                )
                user = auth_response.user
                if user:
                    print("✅ Usuário criado com sucesso!")
                    print("📧 Verifique seu email para confirmação (se necessário)")
                else:
                    print("⚠️  Falha na criação do usuário")
                    return False
            except Exception as signup_error:
                logging.exception(f"Erro ao criar usuário: {signup_error}")
                print(f"❌ Erro ao criar usuário: {signup_error}")
                try:
                    users = supabase.auth.admin.list_users()
                    for u in users:
                        if u.email == admin_email:
                            user = u
                            break
                except Exception as e:
                    logging.exception(f"Erro ao listar usuários: {e}")
                    pass
                if not user:
                    return False
        if not user:
            print("❌ Falha crítica: usuário não foi encontrado nem criado")
            return False
        user_id = user.id
        print(f"🆔 UUID do usuário: {user_id}")
        print("""
📋 Verificando perfil na tabela 'profiles'...""")
        try:
            profile_response = (
                supabase.table("profiles").select("*").eq("user_id", user_id).execute()
            )
            if profile_response.data:
                print("👤 Perfil encontrado. Atualizando role para 'admin'...")
                update_response = (
                    supabase.table("profiles")
                    .update({"role": "admin", "nome": admin_nome})
                    .eq("user_id", user_id)
                    .execute()
                )
                if update_response.data:
                    print("✅ SUCESSO! Usuário promovido a administrador.")
                    print(
                        f"   Role atual: {update_response.data[0].get('role', 'unknown')}"
                    )
                else:
                    raise Exception("Update não retornou dados")
            else:
                print("👤 Perfil não encontrado. Criando novo perfil admin...")
                insert_response = (
                    supabase.table("profiles")
                    .insert({"user_id": user_id, "nome": admin_nome, "role": "admin"})
                    .execute()
                )
                if insert_response.data:
                    print("✅ SUCESSO! Perfil administrativo criado.")
                else:
                    raise Exception("Insert não retornou dados")
        except Exception as profile_error:
            logging.exception(f"Erro ao gerenciar perfil: {profile_error}")
            print(f"⚠️  Erro ao gerenciar perfil: {profile_error}")
            print("""
🛠️  AÇÃO MANUAL NECESSÁRIA:""")
            print("A tabela 'profiles' provavelmente não existe ou não está acessível.")
            print("-" * 60)
            print("Por favor, vá até o SQL Editor do seu projeto Supabase e execute")
            print("o conteúdo do arquivo: app/supabase_schema.sql")
            print("-" * 60)
            print("Isso criará a tabela 'profiles', as políticas de segurança (RLS)")
            print("e os triggers necessários para o funcionamento do sistema.")
        try:
            supabase.auth.sign_out()
        except Exception as e:
            logging.exception(f"Erro no logout: {e}")
            pass
        print(f"\n🎉 Configuração concluída!")
        print(f"\n📝 Credenciais do administrador:")
        print(f"   Email: {admin_email}")
        print(f"   Senha: {admin_password}")
        print(f"\n🚀 Você já pode fazer login na aplicação!")
        return True
    except Exception as e:
        logging.exception(f"Erro inesperado: {e}")
        print(f"\n❌ Erro inesperado: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("🔧 CONFIGURAÇÃO DO USUÁRIO ADMINISTRADOR")
    print("=" * 60)
    success = setup_admin()
    if success:
        print("""
✅ Script executado com sucesso!""")
        sys.exit(0)
    else:
        print("""
❌ Falha na execução do script.""")
        print("Verifique os erros acima e tente novamente.")
        sys.exit(1)