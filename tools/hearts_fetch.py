"""Baixa as fotos dos pedaços de coração para public/coracoes/h<n>.webp.
Mapa em tools/hearts_images.json. Uso: python3 tools/hearts_fetch.py <pasta_cache>"""
import json,subprocess,sys,urllib.request
from pathlib import Path
R=Path(__file__).resolve().parent.parent
cache=Path(sys.argv[1]); cache.mkdir(parents=True,exist_ok=True)
out=R/'public/coracoes'; out.mkdir(parents=True,exist_ok=True)
fail=[]
for n,fig in json.load(open(R/'tools/hearts_images.json')).items():
    if n.startswith('_'): continue
    dst=out/f"h{n}.webp"
    if dst.exists(): continue
    raw=cache/f"{fig}.jpg"
    try:
        if not raw.exists():
            u=f"https://zelda.com.br/wp-content/uploads/games/majoras_mask/site/walkthrough/mm_walkthrough_img{fig}.jpg"
            raw.write_bytes(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"}),timeout=30).read())
    except Exception as ex: fail.append((n,str(ex))); continue
    r=subprocess.run(['magick',str(raw),'-resize','640x480>','-quality','62',str(dst)],capture_output=True,text=True)
    if r.returncode: fail.append((n,r.stderr[:120]))
print('falhas:',fail)
