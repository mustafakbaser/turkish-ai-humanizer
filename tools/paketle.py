#!/usr/bin/env python3
"""Skill'i claude.ai / Claude Desktop'a yüklenebilir bir ZIP olarak paketler.

Yalnızca çalışma zamanında gereken dosyaları alır (testler ve geliştirme
araçları pakete girmez) ve paketlemeden önce SKILL.md ön bilgisini doğrular.

Kullanım:  python3 tools/paketle.py            ->  dist/turkish-ai-humanizer.zip
"""
from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
AD = "turkish-ai-humanizer"
DAHIL = ["SKILL.md", "LICENSE", "references", "scripts/analiz.py", "scripts/kaliplar.json"]
IZINLI_UZANTILAR = {".md", ".py", ".json", ""}  # "" = LICENSE


def on_bilgi_dogrula(skill_md: Path) -> None:
    metin = skill_md.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", metin, re.S)
    if not m:
        sys.exit("SKILL.md ön bilgi (frontmatter) bloğu bulunamadı.")
    on = m.group(1)
    ad = re.search(r"^name:\s*(.+)$", on, re.M)
    aciklama = re.search(r"^description:\s*(.+)$", on, re.M)
    if not ad or not re.fullmatch(r"[a-z0-9-]{1,64}", ad.group(1).strip()):
        sys.exit("name alanı eksik ya da geçersiz (küçük harf, rakam, tire; en fazla 64 karakter).")
    if ad.group(1).strip() != AD:
        sys.exit(f"name alanı '{AD}' olmalı.")
    if not aciklama or not (1 <= len(aciklama.group(1).strip().encode("utf-8")) <= 1024):
        sys.exit("description alanı eksik ya da 1024 bayttan uzun.")
    if re.search(r"<[^>]+>", aciklama.group(1)):
        sys.exit("description alanı XML/HTML etiketi içeremez.")


def _pakete_girer(yol: Path) -> bool:
    """Gizli dosyalar (.DS_Store), önbellekler ve sembolik bağlantılar pakete girmez."""
    goreli = yol.relative_to(KOK)
    if any(parca.startswith(".") or parca == "__pycache__" for parca in goreli.parts):
        return False
    if yol.is_symlink():
        return False
    return yol.is_file()


def dosyalar():
    for oge in DAHIL:
        yol = KOK / oge
        if yol.is_symlink():
            sys.exit(f"Sembolik bağlantı paketlenmez: {oge}")
        if yol.is_dir():
            for p in sorted(yol.rglob("*")):
                if not _pakete_girer(p):
                    continue
                if p.suffix not in IZINLI_UZANTILAR:
                    sys.exit(f"Beklenmeyen dosya türü: {p.relative_to(KOK)}")
                yield p
        elif yol.is_file():
            yield yol
        else:
            sys.exit(f"Eksik dosya: {oge}")


def main() -> int:
    on_bilgi_dogrula(KOK / "SKILL.md")
    hedef = KOK / "dist" / f"{AD}.zip"
    hedef.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(hedef, "w", zipfile.ZIP_DEFLATED) as z:
        for yol in dosyalar():
            z.write(yol, f"{AD}/{yol.relative_to(KOK).as_posix()}")
    with zipfile.ZipFile(hedef) as z:
        adlar = z.namelist()
    print(f"{hedef.relative_to(KOK)} oluşturuldu ({len(adlar)} dosya, {hedef.stat().st_size // 1024} KB)")
    for a in adlar:
        print(f"  {a}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
