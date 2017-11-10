# Segmentation tools
## Introduction
This is a simple tools for visualizing the labels from the output of image semantic segmentations.
## Install
Install dependencies:
* OpenCV
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

Another usage is drawing the labels from the annotations of semantic segmentation in the python script.

```python=
from label_loader import *

mat_file = './my_label.mat'
colors, texts = load_label(mat_file)  #load labels from .mat file
...

anno = sess.run(pred)

seg_color = draw_anno(anno)  # draw colour seg image from annotations
seg_label = draw_labels(anno) # draw label image from annotations
# use can simply blend up the colour seg image with original image
blend = original_img * 0.5 + seg_color * 0.5 

cv2.imwrite(color_path, seg_color)
cv2.imwrite(label_path, seg_label)
cv2.imwrite(blend_path, blend)
...

```

## Result
ADE20K with column size=15

