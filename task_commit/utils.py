import subprocess


def color_text(text, color):
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'reset': '\033[0m',
    }
    return f'{colors.get(color, colors["reset"])}{text}{colors["reset"]}'


def get_git_user():
    try:
        username = subprocess.check_output(
            ['git', 'config', 'user.name'], text=True
        ).strip()
        if not username:
            raise ValueError('Nome de usuário não configurado')
        return username
    except (subprocess.CalledProcessError, ValueError) as e:
        print(color_text(f'❌ Erro ao obter usuário do Git: {e}', 'red'))
        return None


def check_git_status():
    try:
        status = subprocess.check_output(
            ['git', 'status', '--porcelain'], text=True
        ).strip()
        return bool(status)
    except subprocess.CalledProcessError as e:
        print(color_text(f'❌ Erro ao verificar status do Git: {e}', 'red'))
        return False


def is_git_flow():
    try:
        subprocess.check_output(['git', 'flow', 'config'], text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(color_text(f'❌ Gitflow não instalado, mas o push é realizado: {e}', 'red'))
        return False


def get_current_branch():
    try:
        return subprocess.check_output(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'], text=True
        ).strip()
    except subprocess.CalledProcessError as e:
        print(color_text(f'❌ Erro ao obter branch atual: {e}', 'red'))
        return None


def add_changes():
    try:
        subprocess.run(['git', 'add', '.'], check=True)
        print(color_text('✔️ Todas as mudanças adicionadas.', 'green'))
    except subprocess.CalledProcessError as e:
        print(color_text(f'❌ Erro ao adicionar mudanças: {e}', 'red'))
        raise


def create_commit(commit_type, module, commit_message, git_user):
    full_commit_message = f'{commit_type}({module}): {commit_message}'
    updated_commit_message = (
        f'{full_commit_message} (👤 user: {git_user})'.lower()
    )
    try:
        subprocess.run(
            ['git', 'commit', '-m', updated_commit_message], check=True
        )
        print(color_text('✅ Commit realizado com sucesso!\n', 'green'))
    except subprocess.CalledProcessError as e:
        print(color_text(f'❌ Erro ao realizar commit: {e}', 'red'))
        raise


def handle_git_flow(branch):
    action = (
        input(
            color_text(
                "🛠️ Deseja 'publish' ou 'finish' essa branch? "
                '(publish/finish): ',
                'blue',
            )
        )
        .strip()
        .lower()
    )
    if action == 'publish':
        try:
            subprocess.run(
                ['git', 'flow', branch.split('/')[0], 'publish'], check=True
            )
            print(color_text('✅ Publish realizado no Git Flow!\n', 'green'))
        except subprocess.CalledProcessError as e:
            print(color_text(f'❌ Erro ao publicar branch: {e}', 'red'))
    elif action == 'finish':
        try:
            subprocess.run(
                ['git', 'flow', branch.split('/')[0], 'finish'], check=True
            )
            print(color_text('✅ Finish realizado no Git Flow!\n', 'green'))
        except subprocess.CalledProcessError as e:
            print(color_text(f'❌ Erro ao finalizar branch: {e}', 'red'))
    else:
        print(color_text('❌ Ação inválida!', 'red'))


def execute_push(branch):
    try:
        subprocess.run(['git', 'push', 'origin', branch], check=True)
        print(
            color_text(f'✅ Push realizado para a branch {branch}!\n', 'green')
        )
    except subprocess.CalledProcessError as e:
        print(color_text(f'❌ Erro ao fazer push: {e}', 'red'))
