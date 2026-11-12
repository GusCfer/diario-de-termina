import sys,glob,trimesh,numpy as np
from trimesh.transformations import rotation_matrix
for n in sys.argv[2:]:
    f=glob.glob(f"{sys.argv[1]}/m3d/{n}/*.dae")[0]
    sc=trimesh.load(f,force='scene'); sc.apply_transform(rotation_matrix(-np.pi/2,[1,0,0]))
    sc.export(f"{sys.argv[1]}/glb/{n}.glb"); print(n,'ok')
