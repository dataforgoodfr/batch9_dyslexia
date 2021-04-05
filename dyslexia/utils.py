def test_img_fn(images_path, fn, **kwargs):
    for fpath in images_path:
        img_orig = load_image(fpath)
        
        img = fn(img_orig, **kwargs)
        
        print(fpath)
        plot_2_images(img_orig, img)

def reduce_size(img, min_size=None, ratio=None):
    w, h = img.size
    
    if min_size:
        if w < h:
            new_w = min_size
            new_h = w * min_size / h
        else:
            new_h = min_size
            new_w = h * min_size / w
            
    else:
        new_w = w * ratio
        new_h = h * ratio
            
    img = img.resize((int(new_w), int(new_h)), Image.ANTIALIAS)
            
    return img