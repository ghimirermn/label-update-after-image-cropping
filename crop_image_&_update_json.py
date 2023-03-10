import json
import glob
import cv2
import labelme
import base64
import os
from tqdm import tqdm

def base64imgdata(img_path):
    """ returns image as base64 data, required for labelme format """
    data = labelme.LabelFile.load_image_file(img_path)
    image_data = base64.b64encode(data).decode('utf-8')
    return image_data

def conversion(images, annotations):
    """"
    Args:
        images(list) : list of image files
        annotations(list) : list of label files

    Returns:
        cropped images
        json files: new json file(s) with updated annotation format based on cropping of image
    """
    for l in tqdm(range(len(annotations))):
        img = cv2.imread(images[l])

        # (0,0) is the top left corner of image with left-to-right as x-direction and top-to-bottom as y-direction
        #(x1,y1) is top left vertex & (x2,y2) is bottom right vertex

        x1 = (15/100) * img.shape[0]
        x2 = (85/100) * img.shape[0]
        y1 = (20/100) * img.shape[1]
        y2 = (78/100) * img.shape[1]

        # crop = img[start_row:end_row, start_col:end_col]
        crop_img = img[int(x1):int(x2), int(y1):int(y2)]

        cv2.imwrite(os.path.join("updated", os.path.basename(images[l])), crop_img)

        with open(annotations[l]) as f:
            data = json.load(f)

        for k in range(len(data["shapes"])):
            data['shapes'][k]['points'][0][0] = data['shapes'][k]['points'][0][0] - y1
            data['shapes'][k]['points'][1][0] = data['shapes'][k]['points'][1][0] - y1
            data['shapes'][k]['points'][0][1] = data['shapes'][k]['points'][0][1] - x1
            data['shapes'][k]['points'][1][1] = data['shapes'][k]['points'][1][1] - x1

        data['imageData'] = base64imgdata(os.path.join("updated", os.path.basename(images[l])))

        with open(os.path.join("updated", os.path.basename(annotations[l])), "w") as fp:
            json.dump(data, fp, indent=2)

if __name__ == "__main__":
    images = ([i for i in glob.glob("dogs/*.jpg")]) #list of image files
    annotations = [i for i in glob.glob("dogs/*.json")] #list of annotation files
    images.sort()
    annotations.sort()
    conversion(images, annotations)
