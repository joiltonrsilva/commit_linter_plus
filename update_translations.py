import os
import subprocess
import sys
from pathlib import Path

from task_commit.utils import color_text

LOCALES_DIR = "locale"
POT_FILE = os.path.join(LOCALES_DIR, "messages.pot")
PO_FILE = os.path.join(LOCALES_DIR, "pt_BR/LC_MESSAGES/messages.po")
MO_FILE = os.path.join(LOCALES_DIR, "pt_BR/LC_MESSAGES/messages.mo")
SOURCE_DIR = "task_commit"

LANGUAGES = {
    "af": "Afrikaans",
    "ar": "Arabic",
    "az": "Azerbaijani",
    "be": "Belarusian",
    "bg": "Bulgarian",
    "bn": "Bengali",
    "bs": "Bosnian",
    "ca": "Catalan",
    "cs": "Czech",
    "cy": "Welsh",
    "da": "Danish",
    "de": "German",
    "el": "Greek",
    "en": "English",
    "eo": "Esperanto",
    "es": "Spanish",
    "et": "Estonian",
    "eu": "Basque",
    "fa": "Persian",
    "fi": "Finnish",
    "fo": "Faroese",
    "fr": "French",
    "ga": "Irish",
    "gl": "Galician",
    "gu": "Gujarati",
    "he": "Hebrew",
    "hi": "Hindi",
    "hr": "Croatian",
    "hu": "Hungarian",
    "hy": "Armenian",
    "id": "Indonesian",
    "is": "Icelandic",
    "it": "Italian",
    "ja": "Japanese",
    "ka": "Georgian",
    "kk": "Kazakh",
    "km": "Khmer",
    "kn": "Kanari",
    "ko": "Korean",
    "lt": "Lithuanian",
    "lv": "Latvian",
    "mk": "Macedonian",
    "ml": "Malayalam",
    "mn": "Mongolian",
    "mr": "Marathi",
    "ms": "Malay", "mt": "Maltese",
    "nb": "Norwegian Bokmål",
    "ne": "Nepali",
    "nl": "Dutch",
    "nn": "Norwegian Nynorsk",
    "pa": "Punjabi",
    "pl": "Polish",
    "pt": "Portuguese",
    "pt_BR": "Portuguese (Brazil)",
    "pt_PT": "Portuguese (Portugal)",
    "ro": "Romanian",
    "ru": "Russian",
    "si": "Sinhala",
    "sk": "Slovak",
    "sl": "Slovene",
    "sq": "Albanian",
    "sr": "Serbian",
    "sv": "Swedish",
    "sw": "Swahili",
    "ta": "Tamil",
    "te": "Telugu", "th": "Thai",
    "tr": "Turkish",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "vi": "Vietnamese",
    "zh_CN": "Simplified Chinese",
    "zh_TW": "Traditional Chinese",
    "zu": "Zulu"
}


def find_file(file, path):
    caminho = list(Path(path).rglob(file))
    return caminho[0] if caminho else None


def find_python_files(directory):
    """Percorre o diretório e retorna uma lista de todos os arquivos .py."""
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    return python_files


def run_command(command):
    """Executa um comando do sistema e verifica se ocorreu um erro."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(color_text(f"❌ Error executing: {command}\n{result.stderr}", "red"))
        sys.exit(1)


def update_translations():
    """Gera o arquivo POT e atualiza as traduções existentes."""
    # Descobre automaticamente todos os arquivos Python no projeto
    args = sys.argv
    args = args[1:] if len(args) > 1 else None
    if args:
        print(args[0])
        match args[0]:
            case "addlanguage":
                print("Adicionando idioma")

                language = args[1] if len(args) > 1 else None
                if not language:
                    print(color_text("❌ Invalid language", "red"))
            case "help":
                print(
                    "\n\nCommands:\n"
                        "\n- python update_translations.py addlanguage [language]\n"
                          "\tExample: python update_translations.py add_language pt_BR\n"
                        "- python update_translations.py help: help\n"
                        "- python update_translations.py: update translations\n"
                )
            case _:
                print(color_text("❌ Invalid command", "red"))
        return 0
    else:
        source_files = find_python_files(SOURCE_DIR)

        print(color_text("📂 Python files found:", "green"))
        for file in source_files:
            print(color_text(f"  📄 {file}", "green"))

        if not source_files:
            print(color_text("⚠️ No Python files found for extraction.", "red"))
            return

        # Extraindo novas strings para o arquivo .pot
        print(color_text("📥 Extracting strings to .pot file...", "green"))
        run_command(f"xgettext -o {POT_FILE} {' '.join(source_files)}")

        # Atualizando o arquivo .po sem perder traduções anteriores
        if os.path.exists(PO_FILE):
            print(color_text("📦 Updating existing translations...", "green"))
            run_command(f"msgmerge --update {PO_FILE} {POT_FILE}")
        else:
            print(f"⚠️ Arquivo {PO_FILE} não encontrado. Criando um novo.")

        # Compilando o arquivo .mo
        print(color_text("📦 Compiling .mo file...", "green"))
        run_command(f"msgfmt -o {MO_FILE} {PO_FILE}")
        run_command(f"rm {POT_FILE}")

        # Removendo arquivos .po~
        if find_file("messages.po~", LOCALES_DIR):
            os.remove(find_file("messages.po~", LOCALES_DIR))

        print(color_text("✅ Translations updated successfully!", "green"))


if __name__ == "__main__":
    update_translations()
