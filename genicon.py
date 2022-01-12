# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
genicon (https://github.com/HSL5430/app-icon-generator),
forked from (https://github.com/aillieo/app-icon-generator)
Fast and easy way to generate icons for iOS and Android apps
Created by Aillieo on 2017-08-10
With Python 3.5
"""

from PIL import Image
import os
import sys


def help():
    print('Usage:')
    print('1.get reference image by finding one image file in current directory or manually input, and then you will get the icons generated in the ./outputs directory.')
    print('python %s' % sys.argv[0])
    print('2.Support custom <input image path>, and then output to the ./outputs directory under the directory where the input image is located.')
    print('python %s <input image path>' % sys.argv[0])
    print('3.Support custom <outputs directory>.')
    print('python %s <input image path> <outputs directory> ' % sys.argv[0])
    print('In addition, you can read the README.md file!')


def genLauncherIconForAndroid(iconDir):
    return os.path.join(iconDir, 'ic_launcher')


# output path and size config:
path_Android = [
    genLauncherIconForAndroid('mipmap-xxxhdpi'),
    genLauncherIconForAndroid('mipmap-xxhdpi'),
    genLauncherIconForAndroid('mipmap-xhdpi'),
    genLauncherIconForAndroid('mipmap-hdpi'),
    genLauncherIconForAndroid('mipmap-mdpi'),
]
size_Android = [192, 144, 96, 72, 48]

path_iOS = [
    'Icon-57',
    'Icon-114',
]
size_iOS = [57, 114]

path_custom = [
    'my_icon',
    'your_icon',
]
size_custom = [60, 100]

# generate options and params:
auto_overwrite = True

gen_for_iOS = False
# 本人Android开发，所以这里默认True，可根据实际使用频率调整
gen_for_Android = True

need_frame = False
frame_width_ratio = float(30) / 512
frame_radius_ratio = float(90) / 512
frame_color = (255, 255, 255)

need_rounded = True
rounded_radius_ratio = float(90) / 512


def get_input_file():
    """get reference image by finding one image file in current directory or manually input"""
    ref_file = ''
    if len(sys.argv) > 1 and len(sys.argv[1]) > 0:
        ref_file = sys.argv[1]
    else:
        file_ext = ['png', 'jpg', 'jpeg']
        files = os.listdir('.')
        for filename in files:
            if filename.split('.')[-1].lower() in file_ext:
                ref_file = filename
                break
    if ref_file:
        print('Will use "%s" as reference image' % ref_file)
    else:
        print('Can not find property file, now please specific one')
        ref_file = input('input file name:')
    if not os.path.exists(ref_file):
        raise IOError('file not found: ' + ref_file)
    return ref_file


def get_outputs_dir(ref_file):
    outputs = ''
    if len(sys.argv) > 2 and len(sys.argv[2]) > 0:
        outputs = sys.argv[2]
    else:
        outputs = os.path.join(os.path.dirname(ref_file), "outputs")
    return outputs


def gen_template_img(ref_file):
    """get template image for later resizing"""
    template_img = Image.open(ref_file)
    size = min(template_img.width, template_img.height)
    template_img = template_img.resize((size, size), Image.BILINEAR)
    if need_frame:
        template_img = add_frame(template_img)
    if need_rounded:
        template_img = round_corner(template_img)
    return template_img


def gen_icons(ref_file, template_img, dict_path_size):
    """generate icons by resizing template image according to sizes defined in size list"""
    for name, size in dict_path_size:
        name = os.path.join(get_outputs_dir(ref_file), name + '.png')
        name = os.path.normpath(name)
        path, base = os.path.split(name)
        if path and not os.path.exists(path):
            os.makedirs(path)
        out_img = template_img.resize((size, size), Image.BILINEAR)
        if auto_overwrite or not os.path.exists(name):
            try:
                out_img.save(name, 'PNG')
            except IOError:
                print("IOError: save file failed: " + name)
        else:
            print('File already exists: %s , set "auto_overwrite" True to enable overwrite' % name)


def round_corner(img_in):
    """rounding corner for template"""
    if img_in.mode != 'RGBA':
        img_in = img_in.convert('RGBA')
    size = img_in.size[0]
    radius = size * rounded_radius_ratio
    if radius > 0 and rounded_radius_ratio < 0.5:
        img_in.load()
        for i in range(size):
            for j in range(size):
                if in_corner(size, radius, i, j):
                    img_in.putpixel((i, j), (0, 0, 0, 0))
        print("Round corner finished!")
    else:
        print('Round corner failed due to invalid parameters, please check "rounded_radius_ratio"')
    return img_in


def add_frame(img_in):
    """adding frame for template"""
    size = img_in.size[0]
    width = size * frame_width_ratio
    radius = size * frame_radius_ratio
    if radius > 0 and frame_radius_ratio < 0.5 and frame_width_ratio < 0.5:
        img_in.load()
        for i in range(size):
            for j in range(size):
                if in_frame(size, width, radius, i, j):
                    img_in.putpixel((i, j), frame_color)
        print("Add frame finished!")
    else:
        print('Add frame failed due to invalid parameters, please check "frame_width_ratio" and "frame_radius_ratio"')
    return img_in


def in_corner(size, radius, x, y, base_offset=0):
    """judge whether a point is corner of icon"""
    x -= base_offset
    y -= base_offset
    center = (0, 0)
    if x < radius and y < radius:
        center = (radius, radius)
    elif x < radius and y > size - radius:
        center = (radius, size - radius)
    elif x > size - radius and y < radius:
        center = (size - radius, radius)
    elif x > size - radius and y > size - radius:
        center = (size - radius, size - radius)

    if center != (0, 0):
        if (x - center[0])**2 + (y - center[1])**2 > radius**2:
            return True
    return False


def in_frame(size, width, radius, x, y):
    """judge whether a point should be set frame color"""
    inner_rect = width < x < size - width and width < y < size - width
    if not inner_rect:
        return True
    else:
        return in_corner(size - 2 * width, radius - width, x, y, width)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg1 = sys.argv[1].lower()
        if "help" == arg1 or "h" == arg1:
            help()
            exit()

    ref_file = get_input_file()
    img = gen_template_img(ref_file)
    if gen_for_iOS:
        print('Generating for iOS...')
        dict_iOS = zip(path_iOS, size_iOS)
        gen_icons(ref_file, img, dict_iOS)
    if gen_for_Android:
        print('Generating for Android...')
        dict_Android = zip(path_Android, size_Android)
        gen_icons(ref_file, img, dict_Android)
    if not gen_for_iOS and not gen_for_Android:
        print('Generating custom icons...')
        dict_custom = zip(path_custom, size_custom)
        gen_icons(ref_file, img, dict_custom)
    print('Generated icons in the dir: ' + os.path.abspath(get_outputs_dir(ref_file)))
