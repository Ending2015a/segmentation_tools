import cv2
import numpy as np
import math
import scipy.io as sio



#===========LABEL VISUALIZER==============

font_scale = 0.5
font_Face = cv2.FONT_HERSHEY_SIMPLEX

#rgb
label_to_colours = []

label_to_texts = []

def get_label_max_length(label, texts):
    size = len(label)
    maxsz=0
    for k in texts:
        maxsz = len(k)

    return size, maxsz


def center_text(img, text, color, rect):
    text = text.strip()
    font = font_Face
    textsz = cv2.getTextSize(str(text), font, font_scale, 1)[0]

    textX = (rect.w-textsz[0]) // 2 + rect.x
    textY = (rect.h+textsz[1]) // 2 + rect.y


    cv2.putText(img, text, (textX, textY), font, font_scale, [0, 0, 0], 2)
    cv2.putText(img, text, (textX, textY), font, font_scale, color, 1)
    return img

def draw_label_with_text(labels, texts, columns=15):
    size, maxsz = get_label_max_length(labels, texts)

    column = min(size, columns)
    row = int(math.ceil(size/float(columns)))

    wnd_w = (maxsz*10+50)
    wnd_h = 30
    width = row * wnd_w
    height = column * wnd_h

    img = np.zeros((height, width, 3), np.uint8)
    
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
            

    r = rect(wnd_w, wnd_h, column, row)

    for color, text in zip(labels, texts):
        
        color = color.astype(dtype=int).tolist()[::-1]
        cv2.rectangle(img, (r.x, r.y), (r.x+r.w, r.y+r.h), color ,-1)
        img = center_text(img, text, [255, 255, 255], r)
        r.next()


    return img


def draw_labels(anno_img, columns=15):
    color_idx = np.unique(anno_img).astype(int)
    color_list = []
    text_list = []
    for i in color_idx:
        color_list.append(label_to_colours[i])
        text_list.append(label_to_texts[i])

    img = draw_label_with_text(color_list, text_list, columns)
    return img

def draw_anno(anno_img):
    shape = anno_img.shape
    img = np.zeros((shape[0], shape[1], 3), dtype=np.uint8)
    for i in range(shape[0]):
        for j in range(shape[1]):
            img[i, j, :] = label_to_colours[anno_img[i, j]][::-1]
    return img

def draw_anno_and_labels(anno_img, columns=15):
    label = draw_labels(anno_img, columns)
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

def output_all_labels(path, columns=15):
    global label_to_colours
    global label_to_texts
    l = draw_label_with_text(label_to_colours, label_to_texts, columns)
    cv2.imwrite(path, l)

def output_labels(anno_img, path, columns=15):
    l = draw_labels(anno_img, columns)
    cv2.imwrite(path, l)

def output_anno(anno_img, path):
    l = draw_anno(anno_img, path)
    cv2.imwrite(path, l)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='draw some labels')
    parser.add_argument('-m', '--mat', type=str, default='', help='a .mat file which contains \'colors\' and \'names\' columns')
    parser.add_argument('-o', '--output', type=str, default='./labels.png', help='output path of label image')
    parser.add_argument('-c', '--columns', type=int, default=15, help='the maximum column size of label image')
    
    args = parser.parse_args()

    assert args.mat != ''
    assert args.output != ''
    
    import os

    input_path = os.path.abspath(args.mat)
    output_path = os.path.abspath(args.output)

    load_label(input_path)
    output_all_labels(output_path, args.columns)
    print('Save label image to: {}'.format(output_path))


