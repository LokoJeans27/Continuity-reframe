"""Package an existing local proxy and JPEG into a private offline viewer.

Does not estimate depth, reconstruct a scene, call models or send data.
"""
import argparse
import base64
import json
import math
from pathlib import Path
import struct


def build(data_path, frame_path, output):
    data = json.loads(Path(data_path).read_text(encoding='utf-8'))
    count, depth = data['count'], data['target_depth']
    if type(count) is not int or not 0 < count <= 100000:
        raise ValueError('count must be an integer in 1..100000')
    if type(depth) not in (int, float) or not math.isfinite(depth) or depth <= 0:
        raise ValueError('target_depth must be finite and positive')
    raw = base64.b64decode(data['buffer'], validate=True)
    if len(raw) != count * 32:
        raise ValueError('Expected eight little-endian float32 values per Gaussian')
    for point in struct.iter_unpack('<8f', raw):
        if not all(map(math.isfinite, point)) or point[6] <= 0:
            raise ValueError('Invalid coordinates or Gaussian scale')
        if not all(0 <= x <= 1 for x in (*point[3:6], point[7])):
            raise ValueError('RGB and opacity must be in 0..1')
    frame = Path(frame_path).read_bytes()
    if len(frame) > 20_000_000 or not frame.startswith(b'\xff\xd8\xff') or not frame.endswith(b'\xff\xd9'):
        raise ValueError('Supply a JPEG frame below 20 MB')
    payload = dict(count=count, target_depth=depth,
                   buffer=base64.b64encode(raw).decode('ascii'),
                   source=base64.b64encode(frame).decode('ascii'))
    template = Path(__file__).with_name('studio.html.template').read_text(encoding='utf-8')
    assert template.count('__CAMERA_DATA__') == 1
    html = template.replace('__CAMERA_DATA__', json.dumps(payload))
    with Path(output).open('x', encoding='utf-8') as f:
        f.write(html)
    return Path(output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', required=True)
    parser.add_argument('--frame', required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    print(build(args.data, args.frame, args.out))
