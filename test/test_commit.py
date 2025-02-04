import subprocess

import pytest

from task_commit.utils import (
    check_git_status,
    color_text,
    create_commit,
    execute_push,
    get_current_branch,
    get_git_user,
    is_git_flow,
)


# Testando a função color_text
@pytest.mark.parametrize(
    ('text', 'color', 'expected_output'),
    [
        ('Hello', 'red', '\033[91mHello\033[0m'),
        ('Hello', 'green', '\033[92mHello\033[0m'),
        ('Hello', 'yellow', '\033[93mHello\033[0m'),
        ('Hello', 'blue', '\033[94mHello\033[0m'),
        ('Hello', 'magenta', '\033[95mHello\033[0m'),
        ('Hello', 'cyan', '\033[96mHello\033[0m'),
        ('Hello', 'reset', '\033[0mHello\033[0m'),
    ],
)
def test_color_text(text, color, expected_output):
    assert color_text(text, color) == expected_output


# Testando a função get_git_user (simulando uma saída do Git)
def test_get_git_user(mocker):
    mocker.patch('subprocess.check_output', return_value='testuser\n')
    assert get_git_user() == 'testuser'


# Testando a função check_git_status (simulando status do Git)
def test_check_git_status(mocker):
    mocker.patch('subprocess.check_output', return_value=' M file1.txt\n')
    assert check_git_status() is True

    mocker.patch('subprocess.check_output', return_value='')
    assert check_git_status() is False


# Testando a função is_git_flow (simulando um erro no git flow)
def test_is_git_flow(mocker):
    mocker.patch(
        'subprocess.check_output',
        side_effect=subprocess.CalledProcessError(1, 'git flow config'),
    )
    assert is_git_flow() is False

    mocker.patch('subprocess.check_output', return_value='flow config')
    assert is_git_flow() is True


# Testando a função get_current_branch
def test_get_current_branch(mocker):
    mocker.patch('subprocess.check_output', return_value='feature/1234\n')
    assert get_current_branch() == 'feature/1234'

    mocker.patch(
        'subprocess.check_output',
        side_effect=subprocess.CalledProcessError(1, 'git rev-parse'),
    )
    assert get_current_branch() is None


# Testando a função create_commit
def test_create_commit(mocker):
    mocker.patch('subprocess.run')

    commit_type = 'feat'
    module = 'core'
    commit_message = 'implement new feature'
    git_user = 'testuser'

    create_commit(commit_type, module, commit_message, git_user)

    # Garantir que a capitalização está correta
    subprocess.run.assert_called_once_with(
        [
            'git',
            'commit',
            '-m',
            'feat(core): implement new feature (👤 user: testuser)',
        ],
        check=True,
    )


# Testando a função execute_push
def test_execute_push(mocker):
    mocker.patch('subprocess.run')
    branch = 'main'

    execute_push(branch)

    subprocess.run.assert_called_once_with(
        ['git', 'push', 'origin', branch], check=True
    )
