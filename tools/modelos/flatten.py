import sys,collada,numpy as np,trimesh
from PIL import Image
from trimesh.transformations import rotation_matrix
S,OUT=sys.argv[1],sys.argv[2]
JOBS={"blast":("Blast Mask","blast_mask.dae","material-01C6A3B9","mask_bomb_00_0.png","mask_bomb_01_1200.png","material-03FBC186"),
      "couple":("Couple's Mask","couples_mask.dae","material-03F838EB","mask_couple_00_0.png","sp_mask_couple__4000.png","material-03BA0043")}
for key,(name,fn,decal_mat,decal_tex,body_tex,body_mat) in JOBS.items():
    d=f"{S}/m3d/{name}/"; m=collada.Collada(d+fn)
    body=Image.open(d+body_tex).convert('RGB'); col=tuple(int(c) for c in np.asarray(body).reshape(-1,3).mean(0))
    dec=Image.open(d+decal_tex).convert('RGBA'); flat=Image.new('RGBA',dec.size,col+(255,)); flat.alpha_composite(dec)
    meshes=[]
    for bg in m.scene.objects('geometry'):
        for p in bg.primitives():
            pos=p.vertex[p.vertex_index].reshape(-1,3)
            if p.material.id.startswith(decal_mat):
                tc=p.texcoordset[0][p.texcoord_indexset[0]].reshape(-1,2)
                mat=trimesh.visual.material.PBRMaterial(baseColorTexture=flat.convert('RGB'),metallicFactor=0,roughnessFactor=0.8,doubleSided=True)
                meshes.append(trimesh.Trimesh(pos,np.arange(len(pos)).reshape(-1,3),visual=trimesh.visual.TextureVisuals(uv=tc,material=mat),process=False))
    sc=trimesh.Scene(meshes); sc.apply_transform(rotation_matrix(-np.pi/2,[1,0,0])); sc.export(f"{OUT}/{key}.glb"); print(key,col)
