"""Validate bundled nonpersonal viewer data without network, writes or inference."""
from pathlib import Path
import base64,json
import cv2
import numpy as np

root=Path(__file__).resolve().parents[2]
ready=root/'examples/camera_intent/ready'
frame=cv2.imread(str(ready/'frame.jpg'));assert frame is not None and frame.shape==(360,640,3)
data=json.loads((ready/'proxy.json').read_text());assert data['count']==57600
points=np.frombuffer(base64.b64decode(data['buffer'],validate=True),dtype='<f4').reshape(-1,8)
assert points.shape==(57600,8) and np.isfinite(points).all()
assert np.all(points[:,6]>0) and np.all((points[:,3:6]>=0)&(points[:,3:6]<=1))
y,x=np.mgrid[1:360:2,1:640:2]
np.testing.assert_allclose(points[:,0]*576/points[:,2]+320,x.ravel(),atol=.0001)
np.testing.assert_allclose(points[:,1]*576/points[:,2]+180,y.ravel(),atol=.0001)
rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)[y,x].reshape(-1,3)
assert np.abs(rgb.astype(float)-points[:,3:6]*255).mean()<5
html=(ready/'studio.html').read_text(encoding='utf8')
embedded,_=json.JSONDecoder().raw_decode(html.split('const DATA=',1)[1])
assert embedded['buffer']==data['buffer'] and embedded['count']==data['count']
assert base64.b64decode(embedded['source'])==(ready/'frame.jpg').read_bytes()
assert '__CAMERA_DATA__' not in html
print('PASS JPEG decode, 57600 finite Gaussians, front reprojection/color alignment and embedded input identity')
