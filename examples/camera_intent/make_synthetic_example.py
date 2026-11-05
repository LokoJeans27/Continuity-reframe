"""Make a synthetic RGB/depth fixture and ready-to-open camera-intent viewer.

No photographs, models, reconstruction, image generation or network are used.
Run from the repository root with the existing NumPy/OpenCV CLI environment.
"""
import argparse,base64,importlib.util,json
from pathlib import Path
import cv2
import numpy as np


def create(destination):
    out=Path(destination);out.mkdir(parents=True,exist_ok=False)
    height,width=360,640
    yy,xx=np.mgrid[:height,:width]
    checker=((xx//40+yy//40)%2).astype(bool)
    rgb=np.empty((height,width,3),np.uint8)
    rgb[:]=[40,65,95];rgb[checker]=[65,105,145]
    depth=np.full((height,width),2.4,np.float32)
    rectangle=(xx>=230)&(xx<410)&(yy>=90)&(yy<270)
    rgb[rectangle]=[235,155,55];depth[rectangle]=1.65
    cv2.putText(rgb,'SYNTHETIC - NOT A RECONSTRUCTION',(26,32),cv2.FONT_HERSHEY_SIMPLEX,.65,(240,240,240),1,cv2.LINE_AA)
    cv2.putText(rgb,'FRONT PLANE',(242,185),cv2.FONT_HERSHEY_SIMPLEX,.5,(25,30,35),1,cv2.LINE_AA)
    assert cv2.imwrite(str(out/'frame.jpg'),cv2.cvtColor(rgb,cv2.COLOR_RGB2BGR),[cv2.IMWRITE_JPEG_QUALITY,95])
    # The two planes are analytic fixture geometry, not inferred from an image.
    y,x=np.mgrid[1:height:2,1:width:2];z=depth[y,x]
    points=np.stack([(x-320)*z/576,(y-180)*z/576,z,*[rgb[y,x,c]/255 for c in range(3)],z*1.1/576,np.full_like(z,.98)],axis=-1).astype('<f4').reshape(-1,8)
    payload={'count':len(points),'target_depth':2.0,'buffer':base64.b64encode(points.tobytes()).decode('ascii')}
    with (out/'proxy.json').open('x') as f:json.dump(payload,f)
    root=Path(__file__).resolve().parents[2]
    spec=importlib.util.spec_from_file_location('studio_builder',root/'ui/camera_intent/build_studio.py');builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
    builder.build(out/'proxy.json',out/'frame.jpg',out/'studio.html')
    print('Created synthetic frame.jpg, proxy.json and studio.html in',out)
    return out


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir',required=True,help='A NEW directory; existing directories are never overwritten')
    create(parser.parse_args().out_dir)
