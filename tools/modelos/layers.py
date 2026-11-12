import sys,collada,numpy as np,trimesh
from PIL import Image
from trimesh.transformations import rotation_matrix
S=sys.argv[1]
JOBS={"Blast Mask":("blast_mask.dae",{"material-01C6A3B9":("mask_bomb_00_0.png","BLEND"),"material-03FBC186":("mask_bomb_01_1200.png","OPAQUE")}),
      "Couple's Mask":("couples_mask.dae",{"material-03F838EB":("mask_couple_00_0.png","BLEND"),"material-03BA0043":("sp_mask_couple__4000.png","OPAQUE")})}
for name,(fn,tmap) in JOBS.items():
    d=f"{S}/m3d/{name}/"; m=collada.Collada(d+fn); sc=trimesh.Scene()
    for bg in m.scene.objects('geometry'):
        for p in bg.primitives():
            key=next(k for k in tmap if p.material is not None and p.material.id.startswith(k))
            tex,mode=tmap[key]
            pos=p.vertex[p.vertex_index].reshape(-1,3); tc=p.texcoordset[0][p.texcoord_indexset[0]].reshape(-1,2)
            im=Image.open(d+tex); im=im.convert('RGBA')
            mat=trimesh.visual.material.PBRMaterial(baseColorTexture=im,metallicFactor=0,roughnessFactor=1,alphaMode=mode,doubleSided=False)
            mesh=trimesh.Trimesh(pos,np.arange(len(pos)).reshape(-1,3),visual=trimesh.visual.TextureVisuals(uv=tc,material=mat),process=False)
            print(name,key,tex,len(pos)//3,im.getextrema()[3])
            sc.add_geometry(mesh,geom_name=key)
    sc.apply_transform(rotation_matrix(-np.pi/2,[1,0,0])); sc.export(f"{S}/glb/{name}.glb")
