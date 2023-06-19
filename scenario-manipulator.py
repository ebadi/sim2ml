import os, glob
from subprocess import check_output
import shutil
import json
from vectorizer import Vectorizer
import datetime
import numpy as np 
import random
import licenseplatedetector
import distance 
import json
import time


passedtime = time.time()


timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
# timestamp = '2023-04-06-16-51-18'
cwd = os.getcwd()
cwd_timestamp  = os.path.join(cwd, 'results', timestamp)
os.mkdir(cwd_timestamp)
import mutation
scenarioCount= 50000

INTERESTING_KEYS = ['X', 'Y', 'Z', 'Roll', 'Pitch', 'Yaw', 
                    'TargetSpeed', 'InitialSpeed', 'MaxSpeed', # 'AcceptanceRadius',
                    'StartDelay', 'Model', 'Color' 'Gender', 'BodyType', 'Accessory',  # 'Reach', 'HorizontalRange',  'VerticalRange',
                    'Aperture', 'FocalLength', 'Exposure', 'ShutterSpeed', 'Iso', 'Fov',
                    #'HorizontalResolution', 'VerticalResolution', # RADAR
                    'Hour', 'Minute', 
                    'Precipitation',
                    'PlateNumber', 
                    'Weather', 
                    ]

if __name__ == "__main__":
    for i in range(1, scenarioCount):
        scenario_id = str(i + 1)
        scenario_id_dir  = os.path.join(cwd_timestamp, "scenario_" + scenario_id)
        os.mkdir(scenario_id_dir)
        annotation_dir = os.path.join(scenario_id_dir, "Annotation")
        os.mkdir(annotation_dir)
        print("running scenario: ", scenario_id, "/", scenarioCount)
        scenario_path =  os.path.join(cwd, "scenario.JSON")
        scenario_path_new = os.path.join(cwd_timestamp , "scenario_" + scenario_id)
        scenario_path_new_json = scenario_path_new + '.json'
        scenario_path_new_vector = scenario_path_new + '.vec.json'

        vec = Vectorizer(scenario_path, INTERESTING_KEYS)
        vec.data['id'] = scenario_id
        vec.data['GeneralSettings']['OutputSettings']['OutputDirectory'] = scenario_id_dir
        # print(vec.data)
        vec_len = vec.len()
        noise_level_vector = [random.uniform(-1, +1) for _ in range( vec_len)] # [0.05 * i * -1 ] * vec_len
        vec.applyNormalisedNoiseVectorWithFunction(noise_level_vector, mutation.mutation_function)
        #print("\nAFTER APPLYING applyNormalisedNoiseVectorWithFunction:", vec)
        #vec.applyNoiseVector([-6512.111157821896, -8250.541920958469, -6549.4744887180295, -6866.176105360008, -6539.682921961959, -6825.150141301219, -8454.134056406852, -8501.801365496016, -7421.35063255108, -2382.051564669224, 7517.276579859137, -817.6509576612184, 540.92452314087, 2023.6037283999676, -1774.0407909710937, -1780.9470359726897, -507.2112934135571, 717.1024771018488, 593.5833144744655, -6.999880653459741, 3.854589567708899e-05, -7.00003181391935, -7.000094608898053, -6.9887756616528804, -6.988673878934151, -6.999874352831284, 0.00068894121318408, 2.157129726579332e-13, 9.186674532202233e-09, 0, 0, 0, 0, 0, 0, 0, -7.44940185546875, 1.8388226052934442e-08, 0, 0, 0, 0, 0, 0, 0, 89.53021240234375, 134.01441955566406, 134.01441955566406, 134.01441955566406, 134.01441955566406, 134.01441955566406, -127.97929382324219, 32.65242385864258, -60.39958190917969, 50, 50, 50, 50, 50, 50, 1, 1, 1, 1, 1, 1, 0, 0, 20, 10, 0, 0, 'Model 3', 'Type1', 'Purse', 9999, 25, 22, 0, 2, 3, 5001, 12, 126, 98, 16, 34, 10, 1, 'Sunny', 'GAFGM2'])
        vec.save(scenario_path_new_json, scenario_path_new_vector)
        # print("\nAFTER APPLYING applyNoiseVector:", vec)
        print("TIME before Sim init: ",  time.time()  - passedtime )
        passedtime = time.time()
        check_output(".\\Deccq_V3.0.0.5\\Deccq.exe -scenario=\"" + scenario_path_new_json + "\"", shell=True)
        print("TIME sim finished:",  time.time()  - passedtime )
        passedtime = time.time()
        for imagefile in os.scandir(os.path.join(scenario_path_new, 'Normal')):
            distance_filename = os.path.join(scenario_path_new, 'Annotation', imagefile.name + '.result.json')
            distances = []
            if imagefile.is_file():
                print("\nProcessing Image", imagefile.name)
                result = None
                while result is None:
                    try:
                        json_result = licenseplatedetector.licensePlateDetect(imagefile.path)
                        result_json_file, result_image_file = licenseplatedetector.save_annotation(json_result, imagefile, annotation_dir)
                        segmentation_filename = os.path.join(scenario_path_new, 'PlateSegmentation', imagefile.name)
                        result = distance.get_distance_metrics(result_json_file, segmentation_filename, mutation.validPlateNumbers)
                    except Exception as excepttion_error:
                        print("ERROR: something went wrong!" + str(excepttion_error))
                        pass
                distances.append(result)
            # print("Writing distance info: ", distance_filename )
            with open(distance_filename, "w") as outfile:
                outfile.write(json.dumps(distances, indent=4))
        print("TIME to CAMEA server finished:",  time.time()  - passedtime )
        passedtime = time.time()