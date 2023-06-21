import json
import sys, os, csv

Y = []
if __name__ == '__main__':
    sc = sys.argv[1]
    directory = os.path.join('./results/' , sc)
    for scenario_name in os.listdir(directory):
        f = os.path.join( directory, scenario_name)
        if not os.path.isfile(f):
            Yi = []
            res = []
            for sub in scenario_name.split(','):
                if '=' in sub:
                    res.append(map(str.strip, sub.split('=', 1)))
            res = dict(res)
            Yi = list(res.values())
            for frame_name in os.listdir(os.path.join(directory, scenario_name, 'Normal')):
                frame_result = os.path.join(directory, scenario_name, 'Annotation/') + frame_name + '.result.json'
                try:
                    f = json.load(open(frame_result,))[0]
                    Yi.extend(f.values())
                except Exception as e:
                    print(e)

            Y.append(Yi)
            

# speed, weather, hour, precipitation, #IMAGE1 to IMAGE4 OCR RESULTS --> iou [error =10000], lev[error =20], box_score[error=0], ocr_score[error=0], 


print(Y)
with open(sc + "Y.csv","w+") as my_csv:
    csvWriter = csv.writer(my_csv,delimiter=',')
    csvWriter.writerows(Y)