import os, glob
import time
import requests
import json
import matplotlib
import matplotlib.pyplot as plt
import cv2
matplotlib.use('Agg')
import pickle
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import distance

def licensePlateDetect(image_path):
    # API documentation https://cloud.cognitechna.cz:8080/docs
    # Rate about 20 LPs/s
    # curl -X POST  -F "file=@img.jpg"  https://cloud.cognitechna.cz:8080/process_image_multipart?type=anpr.gate.europe
    # Non-blocking mode
    with open(image_path, 'rb') as f:
        url = 'https://cloud.cognitechna.cz:8080/process_image_multipart?type=anpr.gate.europe'
        files = {'file': f}
        resp = requests.post(url, files=files, verify=False, timeout=10)
        # Check if response OK
        if resp.status_code != requests.codes.ok:
            raise Exception(resp.text)

        json_content = resp.json()[0]
        return json_content


def save_annotation(json_content, imagefile, annotation_dir):
    plt.clf()
    plt.ioff()
    plt.figure(figsize = (16,16), dpi= 256) # 2048 = 128 * 16

    image_path = imagefile.path
    image_name = imagefile.name
    json_result_file = os.path.join(annotation_dir, image_name + '.json')
    image_result_file = os.path.join(annotation_dir, image_name)
    with open(json_result_file, 'w') as file_p:
        json.dump(json_content, file_p)
    print(image_name, ":", json_content['result']['status'])
    points = []
    img = cv2.imread(image_path)
    img_converted = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img_converted)
    for object in json_content['result']['localizedObjectAnnotations']:
        points.append(object['points'])
        for pt in points:
            x1 = [pt[0][0], pt[1][0]]
            y1 = [pt[0][1], pt[1][1]]
            x2 = [pt[1][0], pt[2][0]]
            y2 = [pt[1][1], pt[2][1]]
            x3 = [pt[2][0], pt[3][0]]
            y3 = [pt[2][1], pt[3][1]]
            x4 = [pt[3][0], pt[0][0]]
            y4 = [pt[3][1], pt[0][1]]
            plt.plot(x1, y1, x2, y2, x3, y3, x4, y4, color="green", linewidth=2)

        # plt.axis('off')
        plt.draw()
        plt.savefig(image_result_file, bbox_inches='tight',transparent=True)
        # plt.pause(0.1)
        plt.close()
        # time.sleep(1)
    return (json_result_file, image_result_file)