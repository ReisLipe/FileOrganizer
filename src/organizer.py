import shutil

from pathlib import Path
from datetime import datetime

from extension_mapper import EXTENSION_MAPPING


class DownloadsOrganizer:
    def __init__(self, downloads_path=None, dry_run=False):
        if downloads_path:
            self.downloads_path = Path(downloads_path)
        else:
            self.downloads_path = Path.home() / "Downloads"

        self.dry_run = dry_run
        self.moved_files = []
        self.errors = []

        if not self.downloads_path.exists():
            raise ValueError(f"Folder {self.downloads_path} do not exists!")

    def get_category_extension(self, extension):
        extension_lower = extension.lower()
        for (
            category,
            extensions,
        ) in EXTENSION_MAPPING.items():  # .items() retorna pares (chave, valor)
            if (
                extension_lower in extensions
            ):  # 'extensions' no plural para não sobrescrever o parâmetro
                return category
        return "Outros"

    def should_skip_file(self, file_path):
        is_app = file_path.suffix.lower() in [".app", ".pkg"]
        hidden_file = file_path.name.startswith(".")
        system_file = file_path.name in [".DS_Store", "desktop.ini", "Thumbs.db"]
        directory = file_path.is_dir()

        if is_app:
            return False

        if directory or system_file or hidden_file:
            return True

    def create_category_folder(self, category):  # ← Mudar nome para 'folder'
        category_path = self.downloads_path / category
        if not self.dry_run:
            category_path.mkdir(exist_ok=True)
        return category_path

    def move_file(self, source, destination):
        if destination.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name_parts = destination.stem, timestamp, destination.suffix
            new_name = f"{name_parts[0]}_{name_parts[1]}{name_parts[2]}"
            destination = destination.parent / new_name

        if not self.dry_run:
            shutil.move(str(source), str(destination))

        return destination

    def organize(self):
        print(
            f"{'SIMULATING MODE' if self.dry_run else 'ORGANIZING'} downloads folder..."
        )
        print(f"Folder: {self.downloads_path}\n")

        files = list(self.downloads_path.iterdir())
        for file_path in files:
            try:
                # Verifica se deve pular este arquivo
                if self.should_skip_file(file_path):
                    continue

                # Obtém a extensão e categoria
                extension = file_path.suffix
                if not extension:  # Arquivo sem extensão
                    category = "Sem Extensao"
                else:
                    category = self.get_category_extension(extension)

                # Cria a pasta da categoria
                category_folder = self.create_category_folder(category)

                # Define o destino
                destination = category_folder / file_path.name

                # Move o arquivo
                final_destination = self.move_file(file_path, destination)

                # Registra o movimento
                self.moved_files.append(
                    {
                        "origem": file_path,
                        "destino": final_destination,
                        "categoria": category,
                    }
                )

                print(
                    f"{'📄 Moveria' if self.dry_run else '✅ Movido'}: {file_path.name}"
                )
                print(f"   → 📁 {category}/{final_destination.name}")

            except Exception as e:
                self.errors.append({"arquivo": file_path, "erro": str(e)})
                print(f"❌ Erro com {file_path.name}: {e}")

        return self.moved_files, self.errors

    def generate_report(self):
        """
        Gera um relatório da organização

        Returns:
            String com o relatório
        """
        report = ["\n" + "=" * 50]
        report.append("📊 RELATÓRIO DE ORGANIZAÇÃO")
        report.append("=" * 50)

        if self.dry_run:
            report.append("⚠️  MODO SIMULAÇÃO - Nenhum arquivo foi movido")

        # Estatísticas por categoria
        categories = {}
        for move in self.moved_files:
            cat = move["categoria"]
            categories[cat] = categories.get(cat, 0) + 1

        report.append(f"\n📈 Total de arquivos processados: {len(self.moved_files)}")

        if categories:
            report.append("\n📁 Arquivos por categoria:")
            for cat, count in sorted(categories.items()):
                report.append(f"   • {cat}: {count} arquivo(s)")

        if self.errors:
            report.append(f"\n⚠️  Erros encontrados: {len(self.errors)}")
            for error in self.errors:
                report.append(f"   • {error['arquivo'].name}: {error['erro']}")

        report.append("\n" + "=" * 50)

        return "\n".join(report)

    def undo_last_organization(self, log_file="organization_log.json"):
        """
        Desfaz a última organização baseado em um log
        (Implementação futura)
        """
        # TODO: Implementar função de desfazer
        pass
