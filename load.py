import json
import sys, os
import numpy
X = [] # Input vector
Y = [] # outputs
if __name__ == '__main__':
    sc = sys.argv[1]
    directory = os.path.join('./results/' , sc)
    for scenario_name in os.listdir(directory):
        f = os.path.join( directory, scenario_name)
        if not os.path.isfile(f):

            Xi = json.load(open(os.path.join(directory, scenario_name) + '.vec.json',) )
            Yi = []
            for frame_name in os.listdir(os.path.join(directory, scenario_name, 'Normal')):
                frame_result = os.path.join(directory, scenario_name, 'Annotation/') + frame_name + '.result.json'
                f = json.load(open(frame_result,))[0]
                Yi.extend(f.values())
            # print("SCENARIO:", scenario_name)
            X.append(Xi)
            Y.append(Yi)

print(len(X), len(Y))
numpyX = numpy.array(X)
numpyY = numpy.array(Y)

print(numpyX.shape, numpyY.shape)

numpy.savetxt(sc + "X.csv", numpyX  , delimiter=",")
numpy.savetxt(sc + "Y.csv", numpyY  , delimiter=",")
