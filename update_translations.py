import subprocess
import os
from pathlib import Path

LOCALES_DIR = "locale"
POT_FILE = os.path.join(LOCALES_DIR, "messages.pot")
PO_FILE = os.path.join(LOCALES_DIR, "pt_BR/LC_MESSAGES/messages.po")
MO_FILE = os.path.join(LOCALES_DIR, "pt_BR/LC_MESSAGES/messages.mo")
SOURCE_DIR = "task_commit"


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
        print(f"Erro ao executar: {command}\n{result.stderr}")
        exit(1)


def update_translations():
    """Gera o arquivo POT e atualiza as traduções existentes."""
    # Descobre automaticamente todos os arquivos Python no projeto
    source_files = find_python_files(SOURCE_DIR)

    print("📂 Arquivos Python encontrados:")
    for file in source_files:
        print(f" - 📂 {file}")

    if not source_files:
        print("⚠️ Nenhum arquivo Python encontrado para extração.")
        return

    # Extraindo novas strings para o arquivo .pot
    print("🔄 Extraindo strings para o arquivo .pot...")
    run_command(f"xgettext -o {POT_FILE} {' '.join(source_files)}")

    # Atualizando o arquivo .po sem perder traduções anteriores
    if os.path.exists(PO_FILE):
        print("🔄 Atualizando o arquivo .po com novas traduções...")
        run_command(f"msgmerge --update {PO_FILE} {POT_FILE}")
    else:
        print(f"⚠️ Arquivo {PO_FILE} não encontrado. Criando um novo.")

    # Compilando o arquivo .mo
    print("📦 Compilando as traduções para o arquivo .mo...")
    run_command(f"msgfmt -o {MO_FILE} {PO_FILE}")
    run_command(f"rm {POT_FILE}")

    # Removendo arquivos .po~
    if find_file("messages.po~", LOCALES_DIR):
        os.remove(find_file("messages.po~", LOCALES_DIR))

    print("✅ Traduções atualizadas com sucesso!")


if __name__ == "__main__":
    update_translations()
