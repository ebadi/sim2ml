import numpy as np 
import random
import json
import collections
import nested_lookup

class Vectorizer:
    def __init__(self, json_scenario_path, keys = []):
        fr = open(json_scenario_path, 'r')
        self.data = json.load(fr)
        self.keys = keys
        self.scenarioKeys = [] # e.g. "speed", "carModel"
        self.scenarioValues = [] # e.g. 10, "Tesla"
        self.normalisedNoiseVector = []   # level of noise, values between 0 , +1
        self.scenarioNoisyValues = []   # values in different range and type? e.g. "RED" or -0.74
        self.scenarioNoisyValuesIndx = 0

    def __str__(self):
        return  f"data: {self.data}\n" + \
                f"scenarioKeys: {self.scenarioKeys}\n\n" + \
                f"scenarioValues: {self.scenarioValues}\n\n" + \
                f"normalisedNoiseVector: {self.normalisedNoiseVector}\n\n" + \
                f"scenarioNoisyValues: {self.scenarioNoisyValues}\n\n" + \
                f"data: {self.data}\n\n"
    
    def save(self, json_scenario_path, json_vector_path):
        j_file = open(json_scenario_path , 'w')
        json.dump(self.data, j_file, indent=4)
        v_file = open(json_vector_path , 'w')
        json.dump(self.normalisedNoiseVector, v_file)

    def len(self):
        counter = 0
        for k in self.keys:
            counter = counter + nested_lookup.get_all_keys(self.data).count(k)
        return counter

    def apply_noise_CallBack(self, k, v):
        # print(">>", k, ":", v)
        self.scenarioKeys.append(k)
        self.scenarioValues.append(v)
        new_value = self.mutate_function(k, v, self.normalisedNoiseVector[self.scenarioNoisyValuesIndx] )
        self.scenarioNoisyValues.append(new_value)
        self.scenarioNoisyValuesIndx= self.scenarioNoisyValuesIndx + 1
        return new_value

    def replace_with_noise_CallBack(self, k, v):
        self.scenarioKeys.append(k)
        self.scenarioValues.append(v)
        new_value = self.scenarioNoisyValues[self.scenarioNoisyValuesIndx]
        self.scenarioNoisyValuesIndx= self.scenarioNoisyValuesIndx + 1
        return new_value
    
    # -1 <= normalisedNoiseVector[i] <= +1
    def applyNormalisedNoiseVectorWithFunction(self, normalisedNoiseVector, mutate_function, in_place=True):
        self.normalisedNoiseVector = normalisedNoiseVector
        self.mutate_function = mutate_function
        self.scenarioKeys = []
        self.scenarioValues = []
        self.scenarioNoisyValuesIndx = 0
        return nested_lookup.nested_alter(document=self.data, key=self.keys, wild_alter= False, in_place=in_place,  callback_function=self.apply_noise_CallBack)

    def applyNoiseVector(self, noiseVector, in_place=True):
        self.normalisedNoiseVector = []
        self.scenarioNoisyValues = noiseVector
        self.scenarioKeys = []
        self.scenarioValues = []
        self.scenarioNoisyValuesIndx = 0
        return nested_lookup.nested_alter(document=self.data, key=self.keys, wild_alter= False, in_place=in_place,  callback_function=self.replace_with_noise_CallBack)
