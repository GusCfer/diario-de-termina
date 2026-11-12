import sys,os,glob,trimesh
src,dst=sys.argv[1],sys.argv[2]
for d in sorted(glob.glob(src+'/*/')):
    name=os.path.basename(d.rstrip('/'))
    f=(glob.glob(d+'*.obj')+glob.glob(d+'*.dae'))[0]
    try:
        sc=trimesh.load(f,force='scene')
        out=os.path.join(dst,name+'.glb'); sc.export(out)
        tex=sum(1 for g in sc.geometry.values() if getattr(g.visual,'material',None) is not None and getattr(g.visual.material,'baseColorTexture',getattr(g.visual.material,'image',None)) is not None)
        print(f"{name:24s} geoms={len(sc.geometry)} tex={tex} {os.path.getsize(out)//1024}KB")
    except Exception as e: print(name,'ERRO',e)
