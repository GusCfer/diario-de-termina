"""Baixa e converte as imagens da enciclopédia para public/enc/<id>.webp.
Fontes: Zelda Wiki (cdn.wikimg.net), Hyrule Legends (zelda.com.br). Uso: python3 tools/enc_fetch.py <pasta_cache>"""
import json,hashlib,subprocess,sys,urllib.parse,urllib.request
from pathlib import Path
R=Path(__file__).resolve().parent.parent
cache=Path(sys.argv[1]); cache.mkdir(parents=True,exist_ok=True)
out=R/'public/enc'; out.mkdir(parents=True,exist_ok=True)
UA={"User-Agent":"Mozilla/5.0"}
def url_for(e):
    if e.get('w'):
        t=e['w']; md=hashlib.md5(t.encode()).hexdigest()
        return f"https://cdn.wikimg.net/en/zeldawiki/images/{md[0]}/{md[:2]}/{urllib.parse.quote(t)}"
    if e.get('wt'): return f"https://zelda.com.br/wp-content/uploads/games/majoras_mask/site/walkthrough/mm_walkthrough_img{e['wt']}.jpg"
    return e.get('hl')
fail=[]
for e in json.load(open(R/'tools/enc_images.json')):
    dst=out/f"{e['id']}.webp"
    if dst.exists(): continue
    u=url_for(e)
    if not u: fail.append((e['id'],'sem fonte')); continue
    raw=cache/(e['id']+Path(urllib.parse.urlparse(u).path).suffix)
    try:
        if not raw.exists(): raw.write_bytes(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30).read())
    except Exception as ex: fail.append((e['id'],str(ex))); continue
    alpha=subprocess.run(['magick','identify','-format','%[opaque]',str(raw)+'[0]'],capture_output=True,text=True).stdout.strip()
    if alpha=='False':   # recorte transparente (modelo/arte): corta as bordas e cabe num quadrado
        cmd=['magick',str(raw)+'[0]','-trim','+repage','-resize','360x360>','-quality','80','-define','webp:alpha-quality=90',str(dst)]
    else:                # screenshot
        cmd=['magick',str(raw)+'[0]','-resize','720x540>','-quality','62',str(dst)]
    r=subprocess.run(cmd,capture_output=True,text=True)
    if r.returncode: fail.append((e['id'],r.stderr[:120]))
print('falhas:',fail)
