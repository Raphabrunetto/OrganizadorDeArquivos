# Organizador automatico de arquivos

Script simples para organizar arquivos de uma pasta por tipo.
O script varre a pasta inteira (inclusive subpastas) e ajusta arquivos ja organizados
para o formato final (categoria/data apenas para Imagem e Planilhas). Pastas
`drive-download-*` sao tratadas como raizes separadas e organizadas por dentro.

## Como usar

```bash
python organizador.py --path "C:\Users\raphael\Downloads"
```

Para simular sem mover arquivos:

```bash
python organizador.py --path "C:\Users\raphael\Downloads" --dry-run
```

## Estrutura criada

Cada arquivo vai para uma pasta de categoria. Para Imagem e Planilhas, ele cria
subpastas por data de modificacao. Em pastas `drive-download-*`, a organizacao
acontece dentro da propria pasta:

```
PDF/arquivo.pdf
Imagem/2024-04-12/foto.jpg
Planilhas/2024-04-12/planilha.xlsx

drive-download-20250101T000000Z-001/
  Imagem/2025-01-01/foto.jpg
```

## Tipos suportados

- PDF: `.pdf`
- Imagem: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.webp`
- Video: `.mp4`, `.mkv`, `.avi`, `.mov`, `.wmv`, `.flv`, `.webm`
- Planilhas: `.xls`, `.xlsx`, `.csv`, `.ods`, `.tsv`
