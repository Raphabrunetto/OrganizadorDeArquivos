import argparse
import shutil
from datetime import datetime
from pathlib import Path


CATEGORY_EXTS = {
    "PDF": [".pdf"],
    "Imagem": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"],
    "Video": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"],
    "Planilhas": [".xls", ".xlsx", ".csv", ".ods", ".tsv"],
}

EXT_TO_CATEGORY = {
    ext: category for category, exts in CATEGORY_EXTS.items() for ext in exts
}

DATE_CATEGORIES = {"Imagem", "Planilhas"}
NESTED_ROOT_PREFIXES = ("drive-download-",)


def file_date_folder(path: Path) -> str:
    file_time = datetime.fromtimestamp(path.stat().st_mtime)
    return file_time.strftime("%Y-%m-%d")


def unique_destination(dest_dir: Path, filename: str) -> Path:
    candidate = dest_dir / filename
    if not candidate.exists():
        return candidate
    stem = candidate.stem
    suffix = candidate.suffix
    counter = 1
    while True:
        candidate = dest_dir / f"{stem} ({counter}){suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def is_under_any_root(path: Path, roots: set[Path]) -> bool:
    if not roots:
        return False
    for root in roots:
        if root in path.parents:
            return True
    return False


def organize_directory(
    source_dir: Path,
    destination_root: Path,
    dry_run: bool,
    skip_roots: set[Path],
) -> int:
    moved = 0
    items = list(source_dir.rglob("*"))
    for item in items:
        if not item.is_file():
            continue
        item_resolved = item.resolve()
        if is_under_any_root(item_resolved, skip_roots):
            continue
        category = EXT_TO_CATEGORY.get(item.suffix.lower())
        if not category:
            continue
        if category in DATE_CATEGORIES:
            date_folder = file_date_folder(item)
            dest_dir = destination_root / category / date_folder
        else:
            dest_dir = destination_root / category
        if item.parent.resolve() == dest_dir.resolve():
            continue
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_path = unique_destination(dest_dir, item.name)
        if dry_run:
            print(f"[DRY] {item.name} -> {dest_path.relative_to(source_dir)}")
        else:
            shutil.move(str(item), str(dest_path))
            print(f"Movido: {item.name} -> {dest_path.relative_to(source_dir)}")
        moved += 1
    return moved


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Organizador automatico de arquivos por tipo."
    )
    parser.add_argument(
        "--path",
        default=".",
        help="Pasta a ser organizada (padrao: diretorio atual).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Mostra o que seria movido sem alterar arquivos.",
    )
    args = parser.parse_args()

    source_dir = Path(args.path).expanduser().resolve()
    if not source_dir.exists() or not source_dir.is_dir():
        print(f"Pasta invalida: {source_dir}")
        return 1

    nested_roots = {
        entry.resolve()
        for entry in source_dir.iterdir()
        if entry.is_dir()
        and entry.name.lower().startswith(NESTED_ROOT_PREFIXES)
    }

    moved = organize_directory(source_dir, source_dir, args.dry_run, nested_roots)
    for nested_root in sorted(nested_roots):
        moved += organize_directory(nested_root, nested_root, args.dry_run, set())
    if args.dry_run:
        print(f"[DRY] Total de arquivos que seriam movidos: {moved}")
    else:
        print(f"Total de arquivos movidos: {moved}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
