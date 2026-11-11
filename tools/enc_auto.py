"""Gera src/enc_auto.js (inimigos, mini-chefes e chefes) a partir do texto do Hyrule Legends em tools/enc_src.json."""
import json,re,unicodedata
from pathlib import Path
R=Path(__file__).resolve().parent.parent
src=json.load(open(R/'tools/enc_src.json',encoding='utf8'))
def slug(s):
    s=s.replace("'","")
    s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+','-',s).strip('-')
# ids que já são máscaras ou itens
seen={"deku","fairy","blast","bremen","kafei","kamaro","truth","scents","goron","gero","epona","bunny","romani","garo","captain","stone","zora","circus","gibdo","keaton","postman","couple","allnight","giant","fierce"}
def uid(base):
    i=base; n=2
    while i in seen: i=f"{base}-{n}"; n+=1
    seen.add(i); return i
en=[]
for e in src['enemies']:
    loc=e['loc']
    en.append({"id":uid(slug(e['n'])),"n":e['n'],"pt":e['pt'],"hl":e['img'],"where":loc,
               "atk":e['atk'],"str":e['str'],"tatl":e['tatl']})
# dois "Deku Baba" diferentes no guia: diferencia o segundo pelo local
# imagem do guia que não serve (folha de sprites): usa a da Zelda Wiki
for x in en:
    if x["id"]=="mad-scrub": x["w"]="MM_Deku_Scrub_Model.png"
dk=[x for x in en if x['n']=='Deku Baba']
if len(dk)==2: dk[1]['pt']=dk[1]['pt'] or 'Variação'
DUN={"odolwa":"woodfall-temple","goht":"snowhead-temple","gyorg":"great-bay-temple","twinmold":"stone-tower-temple"}
WHERE={"odolwa":"Woodfall Temple","goht":"Snowhead Temple","gyorg":"Great Bay Temple","twinmold":"Stone Tower Temple"}
mini=[];boss=[]
maj_intro=None
for b in src['bosses']:
    name=b['n']; sub=b['pt']
    if ' - ' in name: name,_,en_sub=name.partition(' - ')
    if b['kind']=='mini':
        mini.append({"id":uid(slug(name)),"n":name,"pt":sub,"hl":b['imgs'][0] if b['imgs'] else "","hl2":b['imgs'][1] if len(b['imgs'])>1 else "","d":b['txt']})
    else:
        if name=="Majora's Mask" and maj_intro is None:
            maj_intro=b; continue
        i=slug(name)
        if name=="Majora's Mask": i="majoras-mask-boss"; d=maj_intro['txt']+b['txt']; img=maj_intro['imgs'][0] if maj_intro['imgs'] else ""
        else: d=b['txt']; img=b['imgs'][0] if b['imgs'] else ""
        e={"id":uid(i),"n":name,"pt":sub,"hl":img,"d":d}
        if i in DUN: e["where"]=WHERE[i]; e["rel"]=[DUN[i]]
        else: e["where"]="Dentro da Lua"; e["rel"]=["moon"]
        if not img:
            e["w"]={"majoras-incarnation":"MM_Majora's_Incarnation_Model.png","majoras-wrath":"MM_Majora's_Wrath_Model.png"}.get(i,"MM_Majora's_Mask_Model.png")
        boss.append(e)
out="/* gerado por tools/enc_auto.py a partir dos guias do Hyrule Legends */\n"
out+="const ENC_ENEMY = "+json.dumps(en,ensure_ascii=False)+";\n"
out+="const ENC_MINI = "+json.dumps(mini,ensure_ascii=False)+";\n"
out+="const ENC_BOSS = "+json.dumps(boss,ensure_ascii=False)+";\n"
(R/'src/enc_auto.js').write_text(out,encoding='utf8')
print(len(en),len(mini),len(boss),[b['id'] for b in boss],[m['id'] for m in mini])
