import sys,collada,numpy as np,trimesh
from PIL import Image
d=sys.argv[1]; m=collada.Collada(d+'/mask_gi_rabbit.dae')
sc=trimesh.Scene()
for g in m.geometries:
  for p in g.primitives:
    t=p.triangleset() if hasattr(p,'triangleset') else p
    V=t.vertex; I=t.vertex_index
    uv=t.texcoordset[0]; UI=t.texcoord_indexset[0]
    pos=V[I].reshape(-1,3); tc=uv[UI].reshape(-1,2)
    faces=np.arange(len(pos)).reshape(-1,3)
    mat=trimesh.visual.material.PBRMaterial(baseColorTexture=Image.open(d+'/rb_cap_00_0.png'),metallicFactor=0,roughnessFactor=1)
    mesh=trimesh.Trimesh(pos,faces,visual=trimesh.visual.TextureVisuals(uv=tc,material=mat),process=False)
    print(len(pos),pos.min(0),pos.max(0))
    sc.add_geometry(mesh)
sc.export(sys.argv[2])
