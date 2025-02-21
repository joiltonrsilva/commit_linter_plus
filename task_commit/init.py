import os
import sys

from .utils import get_git_user, get_translator

_ = get_translator()

HOOKS_DIR = '.git/hooks'
HOOK_NAME = 'commit-msg'
HOOK_PATH = os.path.join(HOOKS_DIR, HOOK_NAME)
GIT_USER = get_git_user()

# Expressão regular para validar commits convencionais
COMMIT_REGEX = (
    r'^(feat|fix|chore|refactor|test|docs|style|ci|perf)(\(.+\))?: .{1,72}$'
)

types = """
build: Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)
ci: Changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs)
docs: Documentation only changes
feat: A new feature
fix: A bug fix
perf: A code change that improves performance
refactor: A code change that neither fixes a bug nor adds a feature
style: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
test: Adding missing tests or correcting existing tests
"""  # noqa: E501
HOOK_SCRIPT = f"""#!/bin/sh
    COMMIT_MSG_FILE=$1
    COMMIT_MSG=$(cat "$COMMIT_MSG_FILE")

    if ! echo "$COMMIT_MSG" | grep -qE '{COMMIT_REGEX}'; then
        echo "❌ Invalid commit message! Use Conventional Commits pattern."
        echo "CHECK COMMIT CONVENTIONS BELOW!: {types}"
        echo "Example: feat(core): Add new functionality"
        exit 1
    fi

    GIT_USER=$(git config --get user.name)
    [ -z "$GIT_USER" ] && GIT_USER="Unknown User"

    # Obtém a branch de origem do merge
    CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

    # Padrões de branch do Git Flow
    if echo "$CURRENT_BRANCH" | grep -Eq "^(feature|hotfix|release)/"; then
        echo "\nCo-authored-by: $GIT_USER" >> "$COMMIT_MSG_FILE"
    fi

    """


def setup_git_hook():
    """Configura o hook de commit-msg para validar mensagens."""
    if not os.path.exists(HOOKS_DIR):
        print(
            _(
                '❌ .git/hooks directory not found. Please run inside a Git repository.'  # noqa: E501
            )
        )
        sys.exit(1)

    with open(HOOK_PATH, 'w', encoding='utf-8') as hook_file:
        hook_file.write(HOOK_SCRIPT)

    os.chmod(HOOK_PATH, 0o755)  # Torna o hook executável
    print(_('✅ Commit-msg hook successfully configured!'))
