#!/usr/bin/env python3

"""
File organizer for macOS Downloads folder
This organizer separetes files for type/extensions in subfolders
"""

import argparse

from organizer import DownloadsOrganizer


def main():
    parser = argparse.ArgumentParser(description="Organizador de Downloads para macOS")
    parser.add_argument(
        "--path", "-p", help="Caminho customizado para a pasta Downloads", default=None
    )
    parser.add_argument(
        "--dry-run",
        "-d",
        action="store_true",
        help="Simula a organização sem mover arquivos",
    )

    args = parser.parse_args()

    try:
        # Cria o organizador
        organizer = DownloadsOrganizer(downloads_path=args.path, dry_run=False)

        # Executa a organização
        moved, errors = organizer.organize()

        # Mostra o relatório
        print(organizer.generate_report())

        # Pergunta confirmação se estava em modo simulação
        if args.dry_run and moved:
            response = input("\n🤔 Deseja executar a organização de verdade? (s/n): ")
            if response.lower() == "s":
                print("\n🚀 Executando organização real...")
                organizer_real = DownloadsOrganizer(
                    downloads_path=args.path, dry_run=False
                )
                organizer_real.organize()
                print(organizer_real.generate_report())

    except Exception as e:
        print(f"❌ Erro: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
