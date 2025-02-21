import os
import subprocess
import sys
from pathlib import Path

import inquirer

from task_commit.utils import color_text, get_translator

LOCALES_DIR = 'locale'
POT_FILE = os.path.join(LOCALES_DIR, 'messages.pot')
PO_FILE = os.path.join(LOCALES_DIR, 'pt_BR/LC_MESSAGES/messages.po')
MO_FILE = os.path.join(LOCALES_DIR, 'pt_BR/LC_MESSAGES/messages.mo')
SOURCE_DIR = 'task_commit'

LANGUAGES = {
    'af': 'Afrikaans',
    'ar': 'Arabic',
    'az': 'Azerbaijani',
    'be': 'Belarusian',
    'bg': 'Bulgarian',
    'bn': 'Bengali',
    'bs': 'Bosnian',
    'ca': 'Catalan',
    'cs': 'Czech',
    'cy': 'Welsh',
    'da': 'Danish',
    'de': 'German',
    'el': 'Greek',
    'en': 'English',
    'eo': 'Esperanto',
    'es': 'Spanish',
    'et': 'Estonian',
    'eu': 'Basque',
    'fa': 'Persian',
    'fi': 'Finnish',
    'fo': 'Faroese',
    'fr': 'French',
    'ga': 'Irish',
    'gl': 'Galician',
    'gu': 'Gujarati',
    'he': 'Hebrew',
    'hi': 'Hindi',
    'hr': 'Croatian',
    'hu': 'Hungarian',
    'hy': 'Armenian',
    'id': 'Indonesian',
    'is': 'Icelandic',
    'it': 'Italian',
    'ja': 'Japanese',
    'ka': 'Georgian',
    'kk': 'Kazakh',
    'km': 'Khmer',
    'kn': 'Kanari',
    'ko': 'Korean',
    'lt': 'Lithuanian',
    'lv': 'Latvian',
    'mk': 'Macedonian',
    'ml': 'Malayalam',
    'mn': 'Mongolian',
    'mr': 'Marathi',
    'ms': 'Malay',
    'mt': 'Maltese',
    'nb': 'Norwegian Bokmål',
    'ne': 'Nepali',
    'nl': 'Dutch',
    'nn': 'Norwegian Nynorsk',
    'pa': 'Punjabi',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'pt_BR': 'Portuguese (Brazil)',
    'pt_PT': 'Portuguese (Portugal)',
    'ro': 'Romanian',
    'ru': 'Russian',
    'si': 'Sinhala',
    'sk': 'Slovak',
    'sl': 'Slovene',
    'sq': 'Albanian',
    'sr': 'Serbian',
    'sv': 'Swedish',
    'sw': 'Swahili',
    'ta': 'Tamil',
    'te': 'Telugu',
    'th': 'Thai',
    'tr': 'Turkish',
    'uk': 'Ukrainian',
    'ur': 'Urdu',
    'vi': 'Vietnamese',
    'zh_CN': 'Simplified Chinese',
    'zh_TW': 'Traditional Chinese',
    'zu': 'Zulu',
}

_ = get_translator()


def find_file(file: str, path: str, list_return: bool = False) -> str | list:
    path = list(Path(path).rglob(file))
    if not list_return:
        return path[0] if path else None
    return path if path else None


def find_python_files(directory) -> list:
    """Walks through the directory and returns a list of all .py files."""
    python_files = []
    python_files.append(__file__.split('/')[-1])
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files


def run_command(command) -> None:
    """Executes a system command and checks if an error occurred."""
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        check=True,
    )
    if result.returncode != 0:
        message: str = _('Error executing command')
        print(color_text(f'❌ {message}: {command}\n{result.stderr}', 'red'))
        sys.exit(1)


def input_language() -> str:
    """Asks the user to input a language code and returns it."""
    languages_choices = [
        {'name': f'{name} ({code})', 'value': code}
        for code, name in LANGUAGES.items()
    ]
    try:
        questions = [
            inquirer.List(
                'language_choices',
                message=_('Choose a language'),
                choices=[lang['name'] for lang in languages_choices],
                carousel=True,
            )
        ]
        answers = inquirer.prompt(questions)
        return next(
            lang['value']
            for lang in languages_choices
            if lang['name'] == answers['language_choices']
        )
    except (KeyboardInterrupt, TypeError):
        print(color_text(f'🚩 {_("Process interrupted. Exiting...")}', 'red'))
        sys.exit(0)
    except Exception as error:
        print(
            color_text(f'❌ {_("Unexpected error occurred")}: {error}', 'red')
        )
        sys.exit(1)


def update_translations() -> None:  # noqa: PLR0912, PLR0915
    """Generates the POT file and updates the existing translations."""
    # Automatically discovers all Python files in the project
    args = sys.argv
    args = args[1:] if len(args) > 1 else None
    if args:
        match args[0]:
            case 'addlanguage':
                language = input_language()

                message: str = _('Adding language')
                print(color_text(f'🌍 {message}: {language}', 'green'))

                if not os.path.exists(LOCALES_DIR):
                    os.mkdir(LOCALES_DIR)

                if not os.path.exists(os.path.join(LOCALES_DIR, language)):
                    os.mkdir(os.path.join(LOCALES_DIR, language))
                else:
                    message: str = _('Language already exists')
                    print(color_text(f'⚠️ {message}', 'yellow'))
                    return

                if not os.path.exists(
                    os.path.join(
                        LOCALES_DIR,
                        language,
                        'LC_MESSAGES',
                    )
                ):
                    os.mkdir(
                        os.path.join(
                            LOCALES_DIR,
                            language,
                            'LC_MESSAGES',
                        )
                    )

                if not os.path.exists(
                    os.path.join(
                        LOCALES_DIR,
                        language,
                        'LC_MESSAGES',
                        'messages.po',
                    )
                ):
                    # Listing all Python files
                    source_files = find_python_files(SOURCE_DIR)
                    if not source_files:
                        message: str = _(
                            'No Python files found for extraction',
                        )
                        print(color_text(f'⚠️ {message}', 'red'))
                        return
                    # Creating the .pot file
                    run_command(
                        f'xgettext -o {POT_FILE} {" ".join(source_files)}',
                    )

                    # Copying the .po file

                    os.system(
                        f'cp {POT_FILE} {
                            os.path.join(
                                LOCALES_DIR,
                                language,
                                "LC_MESSAGES",
                                "messages.po",
                            )
                        }',
                    )

                    # Creating .mo file
                    mo_file: str = os.path.join(
                        LOCALES_DIR,
                        language,
                        'LC_MESSAGES',
                        'messages.mo',
                    )
                    run_command(f'touch {mo_file}')

                    # Removing the .pot file
                    run_command(f'rm {POT_FILE}')

                    message: str = _('Language added successfully!')
                    print(color_text(f'✅ {message}', 'green'))

            case 'update':
                message: str = _('Updating translations...')
                print(color_text(f'📥 {message}', 'green'))
                # Listing all Python files
                source_files = find_python_files(SOURCE_DIR)

                message: str = _('Python files found:')
                print(color_text(f'📂 {message}', 'green'))
                for file in source_files:
                    print(color_text(f'  📄 {file}', 'green'))

                if not source_files:
                    message: str = _('No Python files found for extraction')
                    print(color_text(f'⚠️ {message}', 'red'))
                    return

                # Extracting new strings into the .pot file
                message: str = _('Extracting strings to .pot file...')
                print(color_text(f'📥 {message}', 'green'))
                run_command(f'xgettext -o {POT_FILE} {" ".join(source_files)}')

                # Updating the .po file without losing previous translations
                if os.path.exists(
                    find_file(
                        'messages.po',
                        LOCALES_DIR,
                    )
                ):
                    message: str = _('Updating existing translations...')
                    print(color_text(f'📦 {message}', 'green'))
                    po_files = find_file(
                        'messages.po',
                        LOCALES_DIR,
                        list_return=True,
                    )
                    for po_file in po_files:
                        run_command(f'msgmerge --update {po_file} {POT_FILE}')

                else:
                    message: str = _('File not found:')
                    message_: str = _('Creating a new')
                    print(f'⚠️ {message} {PO_FILE}. {message_}')
                    os.system(
                        f'cp {POT_FILE} {
                            os.path.join(LOCALES_DIR, "messages.po")
                        }'
                    )

                # Compiling the .mo file
                message: str = _('Compiling .mo file...')
                print(color_text(f'📦 {message}', 'green'))
                po_files = find_file(
                    'messages.po',
                    LOCALES_DIR,
                    list_return=True,
                )
                mo_files = find_file(
                    'messages.mo',
                    LOCALES_DIR,
                    list_return=True,
                )
                for mo_file, po_file in zip(mo_files, po_files):
                    print(color_text(f'📦 {mo_file}', 'green'))
                    run_command(f'msgfmt -o {mo_file} {po_file}')

                # Removing the .pot file
                run_command(f'rm {POT_FILE}')

                # Remove files .po~
                if find_file('messages.po~', LOCALES_DIR):
                    list_files: list = find_file(
                        'messages.po~',
                        LOCALES_DIR,
                        list_return=True,
                    )
                    for file in list_files:
                        run_command(f'rm {file}')

                message: str = _('Translations updated successfully!')
                print(color_text(f'✅ {message}', 'green'))

            case 'help':
                print(
                    '\n\nCommands:\n'
                    '\n- python update_translations.py addlanguage [language]\n'  # noqa: E501
                    '\tEx: python update_translations.py add_language pt_BR\n'  # noqa: E501
                    '- python update_translations.py help: help\n'
                    '- python update_translations.py update: update translations\n'  # noqa: E501
                )

            case _:
                message: str = _('Invalid command')
                print(color_text(f'❌ {message}', 'red'))
        return 0
    else:
        message: str = _('No arguments provided')
        print(color_text(f'❌ {message}', 'red'))
        return 1


if __name__ == '__main__':
    update_translations()
