import re
import subprocess


def color_text(text, color) -> str:
    """
    Colors text based on a color string.

    Parameters
    ----------
    text : str
    Text to be placed.
    color : str
    Color of the text. Possible values: "red", "green", "yellow", "blue",
    "magenta", "cyan".

    Returns
    -------
    str
    Text with the color applied.
    """
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


def get_git_user() -> str:
    """
    Gets the Git username.

    Returns
    -------
    str or None
    Git username if found, otherwise None.
    """
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


def check_git_status() -> bool:
    """
    Checks for changes in the Git repository.

    Returns
    -------
    bool
    True if there are changes in the repository, False otherwise.
    """
    try:
        status = subprocess.check_output(
            ['git', 'status', '--porcelain'], text=True
        ).strip()
        return bool(status)
    except subprocess.CalledProcessError as e:
        print(color_text(f'❌ Erro ao verificar status do Git: {e}', 'red'))
        return False


def get_git_status() -> str | None:
    """
    Gets the status of the Git repository.

    Returns
    -------
    str or None
        String with the formatted status of the Git repository if found, otherwise None.
    """
    try:
        output = subprocess.check_output(['git', 'status', '--porcelain'], text=True).strip()

        # if not output:
        #     return color_text("✔ No changes detected", "green")

        changes_not_staged = []
        changes_staged = []
        untracked_files = []

        # Process each line of output
        for line in output.split("\n"):
            status_code, file_path = line[:2].strip(), line[2:].strip()

            if status_code in ("M", "A", "D", "R"):  # Modified, Added, Deleted, Renamed (Staged)
                changes_staged.append(f"{file_path}")
            elif status_code in (" M", " D"):  # Modified or deleted (Not Staged)
                changes_not_staged.append(f"{file_path}")
            elif status_code == "??":  # Untracked files
                untracked_files.append(f"{file_path}")

        # Format the output
        result = []
        if changes_not_staged:
            result.append(color_text("📋 Changes not staged:", "yellow"))
            result.extend(color_text(f"   🎯 {item}", "yellow") for item in changes_not_staged)
            result.append("")
        if changes_staged:
            result.append(color_text("📝 Changes staged:", "green"))
            result.extend(color_text(f"   🎯 {item}", "green") for item in changes_staged)
            result.append("")
        if untracked_files:
            result.append(color_text("❌Untracked files:", "red"))
            result.extend(color_text(f"   🎯 {item}", "red") for item in untracked_files)
            result.append("")

        return "\n".join(result)

    except subprocess.CalledProcessError as e:
        return color_text(f'❌ Erro ao verificar status do Git: {e}', 'red')


def is_git_flow():
    """
    Checks if the repository uses Git Flow.

    Returns
    -------
    bool
    True if the repository uses Git Flow, False otherwise.
    """
    try:
        subprocess.check_output(['git', 'flow', 'config'], text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(
            color_text(
                f'❌ Gitflow não instalado, mas o push é realizado: {e}', 'red'
            )
        )
        return False


def get_current_branch():
    """
    Gets the name of the current branch of the Git repository.

    Returns
    -------
    str or None
    Name of the current branch if found, otherwise None.
    """
    try:
        return subprocess.check_output(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'], text=True
        ).strip()
    except subprocess.CalledProcessError as e:
        print(color_text(f'❌ Erro ao obter branch atual: {e}', 'red'))
        return None


def add_changes():
    """
    Add all changes from the Git repository.

    ------
    subprocess.CalledProcessError
    If there was an error while adding the changes.
    """
    try:
        subprocess.run(['git', 'add', '.'], check=True)
        print(color_text('✔️ Todas as mudanças adicionadas.', 'green'))
    except subprocess.CalledProcessError as e:
        print(color_text(f'❌ Erro ao adicionar mudanças: {e}', 'red'))
        raise


def create_commit(commit_type, module, commit_message, git_user):
    """
    Performs a commit to the Git repository with the specified type,
    module, and message.

    Parameters
    ----------
    commit_type : str
    Commit type:
    (feat, fix, chore, refactor, test, docs, style, ci, perf).
    module : str
    Module that the commit refers to.
    commit_message : str
    Commit message.
    git_user : str
    Git user who performed the commit.

    ------
    subprocess.CalledProcessError
    If there was an error while performing the commit.
    """
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
    """
    Manages the Git Flow workflow for the specified branch.

    Parameters
    ----------
    branch : str
    Name of the branch in "type/name" format that you want to publish
    or finish.

    Prompts the user for the desired action ('publish' or 'finish') for the
    given branch and executes the appropriate Git Flow command.
    Displays success or error messages based on the result of the command
    execution.

    ------
    subprocess.CalledProcessError
    If there is an error executing the Git Flow command.
    """

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
        except subprocess.CalledProcessError as e:
            print(color_text(f'❌ Erro ao publicar branch: {e}', 'red'))
    elif action == 'finish':
        try:
            subprocess.run(
                ['git', 'flow', branch.split('/')[0], 'finish'], check=True
            )
        except subprocess.CalledProcessError as e:
            print(color_text(f'❌ Erro ao finalizar branch: {e}', 'red'))
    else:
        print(color_text('❌ Ação inválida!', 'red'))


def execute_push(branch):
    """
    Pushes the current branch to the remote repository.

    Parameters
    ----------
    branch : str
    Name of the branch you want to push.

    ------
    subprocess.CalledProcessError
    If there is an error during the push.
    """
    try:
        subprocess.run(['git', 'push', 'origin', branch], check=True)
    except subprocess.CalledProcessError as e:
        print(color_text(f'❌ Erro ao fazer push: {e}', 'red'))


def remove_excess_spaces(text: str) -> str:
    """
    Removes excess spaces from text.

    Parameters
    ----------
    text : str
    Text from which to remove excess spaces.

    Returns
    -------
    str
    Text without excess spaces.
    """
    if text is None:
        return ''

    text_without_extra_space: str = re.sub(r'\s+', ' ', text)
    return text_without_extra_space.strip()
