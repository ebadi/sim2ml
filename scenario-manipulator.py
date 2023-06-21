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
# scenarioCount= 50000

def range_with_floats(start, stop, step):
    while stop > start:
        yield start
        start += step

if __name__ == "__main__":
    for weather in ("Sunny", "RainyWithSun", "Rainy", "SnowyWithSun", "Snowy"):  # NOT ORDERED
        for speed in range(125, 50, -25): 
            for hour in range(0, 23, 4): # NOT ORDERED
                for precipitation in range_with_floats(0, 1, 0.25): # For sunny weather this value doesn't make sense
                    scenario_id = "speed=" + str(speed) + ",weather=" + weather  + ",hour=" + str(hour)  + ",precipitation=" + str(precipitation) 
                    scenario_id_dir  = os.path.join(cwd_timestamp, "scenario_" + scenario_id)
                    os.mkdir(scenario_id_dir)
                    annotation_dir = os.path.join(scenario_id_dir, "Annotation")
                    os.mkdir(annotation_dir)
                    print("running scenario: ", scenario_id)
                    scenario_path =  os.path.join(cwd, "scenario.JSON")
                    scenario_path_new = os.path.join(cwd_timestamp , "scenario_" + scenario_id)
                    scenario_path_new_json = scenario_path_new + '.json'
                    scenario_path_new_vector = scenario_path_new + '.vec.json'
                    vec = Vectorizer(scenario_path, None)
                    vec.data['id'] = scenario_id
                    vec.data['GeneralSettings']['OutputSettings']['OutputDirectory'] = scenario_id_dir
                    vec.data['GeneralSettings']['EnvironmentSettings']['Weather'] = weather
                    ## All speeds
                    vec.data['ScenarioActors']['Dynamic']['Vehicles'][0]['InitialSpeed'] = speed
                    vec.data['ScenarioActors']['Dynamic']['Vehicles'][0]['MaxSpeed'] = speed
                    vec.data['ScenarioActors']['Navigation']['Waypoints'][0]['TargetSpeed'] = speed
                    vec.data['ScenarioActors']['Navigation']['Waypoints'][1]['TargetSpeed'] = speed
                    vec.data['ScenarioActors']['Navigation']['Waypoints'][2]['TargetSpeed'] = speed
                    
                    vec.data['GeneralSettings']['EnvironmentSettings']['hour'] = hour
                    vec.data['GeneralSettings']['EnvironmentSettings']['Precipitation'] = precipitation
                    print(vec.data)
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
                                    result = distance.get_distance_metrics(result_json_file, segmentation_filename, [vec.data['ScenarioActors']['Dynamic']['Vehicles'][0]['LicensePlate']['PlateNumber']] )
                                except Exception as excepttion_error:
                                    print("ERROR: something went wrong!" + str(excepttion_error))
                                    pass
                            distances.append(result)
                        print("Writing distance info: ", distance_filename )
                        with open(distance_filename, "w") as outfile:
                            outfile.write(json.dumps(distances, indent=4))
                    print("TIME to CAMEA server finished:",  time.time()  - passedtime )
                    passedtime = time.time()
