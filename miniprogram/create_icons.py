# create_icons.py
# 运行一次即可生成小程序底部导航栏所需的图标文件
# 用法：在 miniprogram 目录下执行 python create_icons.py

import struct
import zlib
import os

def make_solid_png(r, g, b, size=40):
    """生成一个纯色的 PNG 图片（40x40 像素）"""
    w = h = size

    def u32(n):
        return struct.pack('>I', n)

    def make_chunk(name, data):
        crc = zlib.crc32(name + data) & 0xffffffff
        return u32(len(data)) + name + data + u32(crc)

    # PNG 文件头
    signature = b'\x89PNG\r\n\x1a\n'
    # 图像头：宽、高、位深=8、色彩类型=2(RGB)
    ihdr_data = u32(w) + u32(h) + b'\x08\x02\x00\x00\x00'
    ihdr = make_chunk(b'IHDR', ihdr_data)
    # 图像数据：每行前有一个过滤字节 0x00
    raw_rows = b''.join(b'\x00' + bytes([r, g, b]) * w for _ in range(h))
    idat = make_chunk(b'IDAT', zlib.compress(raw_rows))
    iend = make_chunk(b'IEND', b'')

    return signature + ihdr + idat + iend


# 图标颜色定义：灰色=未选中，靛蓝紫=选中
ICONS = {
    'home':          (153, 153, 153),  # 灰色
    'home-active':   (79,  70,  229),  # 主色
    'jd':            (153, 153, 153),
    'jd-active':     (79,  70,  229),
    'resume':        (153, 153, 153),
    'resume-active': (79,  70,  229),
}

output_dir = os.path.join(os.path.dirname(__file__), 'assets', 'icons')
os.makedirs(output_dir, exist_ok=True)

for name, (r, g, b) in ICONS.items():
    path = os.path.join(output_dir, f'{name}.png')
    with open(path, 'wb') as f:
        f.write(make_solid_png(r, g, b))
    print(f'OK: {name}.png')

print('图标生成完毕！现在可以用微信开发者工具打开小程序了。')
