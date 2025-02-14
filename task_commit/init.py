import os
import sys
import re

HOOKS_DIR = ".git/hooks"
HOOK_NAME = "commit-msg"
HOOK_PATH = os.path.join(HOOKS_DIR, HOOK_NAME)

# Expressão regular para validar commits convencionais
COMMIT_REGEX = r"^(feat|fix|chore|refactor|test|docs|style|ci|perf)(\(.+\))?: .{1,72}$"

HOOK_SCRIPT = f"""#!/bin/sh
COMMIT_MSG_FILE=$1
COMMIT_MSG=$(cat "$COMMIT_MSG_FILE")

if ! echo "$COMMIT_MSG" | grep -qE '{COMMIT_REGEX}'; then
    echo "❌ Mensagem de commit inválida! Use o padrão Conventional Commits."
    echo "Exemplo: feat(core): Adiciona nova funcionalidade"
    exit 1
fi
"""

def setup_git_hook():
    """Configura o hook de commit-msg para validar mensagens."""
    if not os.path.exists(HOOKS_DIR):
        print("❌ Diretório .git/hooks não encontrado. Execute dentro de um repositório Git.")
        sys.exit(1)

    with open(HOOK_PATH, "w") as hook_file:
        hook_file.write(HOOK_SCRIPT)

    os.chmod(HOOK_PATH, 0o755)  # Torna o hook executável
    print("✅ Hook de commit-msg configurado com sucesso!")
