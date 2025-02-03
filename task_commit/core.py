from .utils import color_text, get_git_user, check_git_status, add_changes, create_commit, handle_git_flow, execute_push, is_git_flow, get_current_branch

def git_commit():
    try:
        print(color_text("\n🚀 Iniciando processo de commit 🚀\n", "cyan"))
        
        if not check_git_status():
            print(color_text("✅ Não há mudanças para commit.", "green"))
            return

        add_all = input(color_text("📌 Deseja adicionar todas as mudanças? (✅ s / ❌ n) [s]: ", "yellow")).strip().lower() or "s"
        if add_all == 's':
            add_changes()
        elif add_all != 'n':
            print(color_text("❌ Opção inválida!", "red"))
            return
        else:
            print(color_text("❌ Adicione manualmente as mudanças e execute o comando novamente.", "red"))
            return
        
        commit_type = input(color_text("🎯 Escolha o tipo de commit (feat, fix, chore, refactor, test, docs, style, ci, perf): ", "blue")).strip().lower()
        if commit_type not in ["feat", "fix", "chore", "refactor", "test", "docs", "style", "ci", "perf"]:
            print(color_text("❌ Tipo de commit inválido!", "red"))
            return
        
        module = input(color_text("🗂️ Qual módulo foi alterado? (exemplo: core, api, models): ", "magenta")).strip().lower()
        
        commit_message = input(color_text("📝 Digite a mensagem do commit: ", "green")).strip()
        if not commit_message:
            print(color_text("❌ Mensagem de commit é obrigatória!", "red"))
            return
        
        git_user = get_git_user()
        if git_user is None:
            print(color_text("❌ Erro: Nome de usuário do Git não configurado!", "red"))
            return
        
        create_commit(commit_type, module, commit_message, git_user)
        
        push = input(color_text("🚀 Deseja fazer push para o repositório? (✅ s / ❌ n) [s]: ", "yellow")).strip().lower() or "s"
        if push == 's':
            current_branch = get_current_branch()
            if is_git_flow() and current_branch:
                if current_branch.startswith("feature/") or current_branch.startswith("hotfix/") or current_branch.startswith("release/"):
                    handle_git_flow(current_branch)
                else:
                    execute_push(current_branch)
            else:
                execute_push(current_branch)

    except KeyboardInterrupt:
        print("\nSAINDO...")
        exit(0)

    except Exception as error:
        print(color_text(f"❌ Erro inesperado: {error}", "red"))
        exit(1)
