# Segmentation tools
## Introduction
This is a simple tools for visualizing the labels from the output of image semantic segmentations.
## Install
Install dependencies:
* PIL
* Scipy
* Numpy
## Usage
First you need to create your label mapping and save it as `.mat` file which you can use scipy.io to do it. And the format like this:
```python=
#label colors (uint8 R/G/B)
mat_color=[[0, 0, 0],
           [0, 255, 255],
           ...
          ]
# label texts (str)
mat_name=['label A',
          'label B',
          ...
         ]

scipy.io.savemat('my_label.mat', 
                 {'colors':mat_color, 'names': mat_name}
                )
```
Then you can draw it by running `label_loader.py` with `--mat` and `--output`
```
python label_loader.py --mat my_label.mat --output label_pic.png
```

```
-m, --mat [.mat]    : input .mat file 
-o, --output [.png] : output file name
-c, --columns [int] : the maximum column size
```
---

Another usage is drawing the labels from the annotations of segmentation results in the python script.

```python=
from label_loader import *

mat_file = './my_label.mat'
colors, texts = load_label(mat_file)  #load labels from .mat file
...

anno = sess.run(pred)

seg_color = draw_anno(anno)[:,:,::-1]  # colored annotations and convert RGB to BGR
seg_label = draw_labels(anno)[:,:,::-1] # draw label image from annotations and convert RGB to BGR
# use can simply blend up the colour seg image with original image
blend = original_img * 0.5 + seg_color * 0.5 

cv2.imwrite(color_path, seg_color)
cv2.imwrite(label_path, seg_label)
cv2.imwrite(blend_path, blend)
...

```

## Other Functions
```
set_shadow_color(color)
# color: the color of text shadow (RGB)

set_font_color(color)
# color: the color of text (RGB)

set_font_face(font_file):
# you can change your font style if you have any .ttf file
# font_file: .ttf file

set_font_size(size):
# font size

output_all_labels(path, columns=15)
# draw & save all labels in loaded .mat file to the path

output_labels(anno_img, path, columns=15)
# draw & save labels contains in annotations only

output_anno(anno_img, path, columns=15)
# draw & save colored annotation image
```

## Result
ADE20K with column size=15 <br/>
<img src="https://raw.githubusercontent.com/Ending2015a/segmentation_tools/master/image/ade20k_label_15.png" width="600"></img>
<br/>
ADE20K with column size=30 <br/>
<img src="https://raw.githubusercontent.com/Ending2015a/segmentation_tools/master/image/ade20k_label_30.png" width="600"></img>

Cityscapes <br/>

| Image | Seg | Label
|:-----:|:----:|:----:|
| <img src="https://raw.githubusercontent.com/Ending2015a/segmentation_tools/master/image/hanover_000000_027998_leftImg8bit.png" width="300"></img> | <img src="https://raw.githubusercontent.com/Ending2015a/segmentation_tools/master/image/seg.png" width="300"></img> | <img src="https://raw.githubusercontent.com/Ending2015a/segmentation_tools/master/image/label.png" width="200"></img> |




