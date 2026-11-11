"""Monta public/index.html a partir de src/. Uso: python3 build.py"""
from pathlib import Path
src = Path(__file__).parent / "src"
s = (src / "template.html").read_text(encoding="utf8")
s = (s.replace("__IMGS__", (src / "imgs2.json").read_text(encoding="utf8"))
      .replace("__DATA__", (src / "data.js").read_text(encoding="utf8"))
      .replace("__HEARTS__", (src / "hearts.js").read_text(encoding="utf8"))
      .replace("__ENC__", (src / "enc.js").read_text(encoding="utf8") + (src / "enc_auto.js").read_text(encoding="utf8"))
      .replace("__AUTH__", (src / "auth.html").read_text(encoding="utf8")))
out = Path(__file__).parent / "public" / "index.html"
out.write_text(s, encoding="utf8")
print(f"{out} ({len(s)//1024} KB)")
