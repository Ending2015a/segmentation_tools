from PIL import Image, ImageDraw, ImageFont
import numpy as np
import math
import scipy.io as sio
import os


#===========LABEL VISUALIZER==============

font_size = 20
font_face_file = "./font/Arial.ttf"
font_shadow = (0, 0, 0)  # text shadow color
font_color = (255, 255, 255) # text color

#=========================================

font_face_file = os.path.abspath(font_face_file)
font_face = ImageFont.truetype(font_face_file, font_size)


#rgb
label_to_colours = []
label_to_texts = []


def set_shadow_color(color):
    assert(len(color)==3)
    font_shadow = tuple(color)

def set_font_color(color):
    assert(len(color)==3)
    font_color = tuple(color)

def set_font_face(font_file):
    font_face_file = font_file
    font_face = ImageFont.truetype(font_face_file, font_size)

def set_font_size(size):
    font_size = size
    font_face = ImageFont.truetype(font_face_file, font_size)

def get_label_max_length(label, texts):
    size = len(label)
    maxsz=0
    for k in texts:
        maxsz = len(k)

    return size, maxsz


def center_text(draw, text, rect):
    text = text.strip()
    font = font_face
    textsz = font.getsize(str(text))
    #textsz = cv2.getTextSize(str(text), font, font_scale, 1)[0]

    x = (rect.w-textsz[0]) // 2 + rect.x
    y = (rect.h-textsz[1]) // 2 + rect.y


    #cv2.putText(img, text, (textX, textY), font, font_scale, [0, 0, 0], 2)
    #cv2.putText(img, text, (textX, textY), font, font_scale, color, 1)

    draw.text((x-1, y), text, font=font, fill=font_shadow)
    draw.text((x+1, y), text, font=font, fill=font_shadow)
    draw.text((x, y-1), text, font=font, fill=font_shadow)
    draw.text((x, y+1), text, font=font, fill=font_shadow)

    draw.text((x-1, y-1), text, font=font, fill=font_shadow)
    draw.text((x+1, y-1), text, font=font, fill=font_shadow)
    draw.text((x-1, y+1), text, font=font, fill=font_shadow)
    draw.text((x+1, y+1), text, font=font, fill=font_shadow)

    draw.text((x, y), text, font=font, fill=font_color)

    return draw


def draw_label_with_text(labels, texts, column=15):
    size, maxsz = get_label_max_length(labels, texts)

    col = min(size, column)
    row = int(math.ceil(size/float(column)))

    wnd_w = (maxsz*10+50)
    wnd_h = 30
    width = row * wnd_w
    height = col * wnd_h

    #img = np.zeros((height, width, 3), np.uint8)

    img = Image.new('RGB', (width, height), (0, 0, 0))

    draw = ImageDraw.Draw(img)

    class rect:
        def __init__(self, w, h, colmax, rowmax):
            self.x=0
            self.y=0
            self.w=w
            self.h=h
            self.cmax = colmax
            self.rmax = rowmax
            self.c=0
            self.r=0
        def next(self):
            self.y += self.h
            self.c += 1
            if self.c == self.cmax:
               self.x += self.w
               self.r += 1
               self.c = 0
               self.y = 0 
            

    r = rect(wnd_w, wnd_h, col, row)

    for color, text in zip(labels, texts):
        
        color = tuple(color.astype(dtype=int).tolist())
        draw.rectangle([(r.x, r.y), (r.x+r.w-1, r.y+r.h-1)], color)
        #cv2.rectangle(img, (r.x, r.y), (r.x+r.w, r.y+r.h), color ,-1)
        draw = center_text(draw, text, r)
        r.next()

    return img


def draw_labels(anno_img, column=15):
    color_idx = np.unique(anno_img).astype(int)
    color_list = []
    text_list = []
    for i in color_idx:
        color_list.append(label_to_colours[i])
        text_list.append(label_to_texts[i])

    img = draw_label_with_text(color_list, text_list, column)
    return np.array(img)

def draw_anno(anno_img):
    shape = anno_img.shape
    img = np.zeros((shape[0], shape[1], 3), dtype=np.uint8)
    for i in range(shape[0]):
        for j in range(shape[1]):
            img[i, j, :] = label_to_colours[anno_img[i, j]]
    return img

def draw_anno_and_labels(anno_img, column=15):
    label = draw_labels(anno_img, column)
    seg = draw_anno(anno_img)
    return seg, label

def load_label(mat_file):
    import scipy.io as sio
    mat = sio.loadmat(mat_file)
    global label_to_colours
    global label_to_texts
    label_to_colours = mat['colors']
    label_to_texts = mat['names']
    return label_to_colours, label_to_texts

def output_all_labels(path, column=15):
    global label_to_colours
    global label_to_texts
    l = draw_label_with_text(label_to_colours, label_to_texts, column)
    l.save(path)

def output_labels(anno_img, path, column=15):
    l = Image.fromarray(draw_labels(anno_img, columns))
    l.save(path)

def output_anno(anno_img, path):
    l = Image.fromarray(draw_anno(anno_img, path))
    l.save(path)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='draw some labels')
    parser.add_argument('-m', '--mat', type=str, default='', help='a .mat file which contains \'colors\' and \'names\' columns')
    parser.add_argument('-o', '--output', type=str, default='./labels.png', help='output path of label image')
    parser.add_argument('-c', '--column', type=int, default=15, help='the maximum column size of label image')
    
    
    args = parser.parse_args()

    assert args.mat != ''
    assert args.output != ''
    
    import os

    input_path = os.path.abspath(args.mat)
    output_path = os.path.abspath(args.output)

    load_label(input_path)
    output_all_labels(output_path, args.column)
    print('Save label image to: {}'.format(output_path))


