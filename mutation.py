
import random

validBodyType= ["Type1", "Type2","Type3"]
validGender= ["Female","Male"] 
validAccessories= ["Phone", "Purse", "Cup"]
validModels= ["Model 1", "Model 2", "Model 3", "Model 4", "Model 5", "Model 6"]
validPlateNumbers = ['1A2B3C', '4D5E6F', '7G8H9I', '0JKLMN', 'OPQRST', 'UVWZYZ', '1C2F3H', '4J5L6O', '7Q8S9W']
validColors = ['red', 'green', 'white', 'silver', 'grey', 'beige', 'blue', 'black']
validWeathers= ['Sunny', 'SnowyWithSun','RainyWithSun', 'CloudyWithSun'] #  [Weather = Sunny, Rainy, RainyWithSun, Snowy, SnowyWithSun, Random]


def remap( x, oMin, oMax, nMin, nMax ):
    #range check
    nMin = nMin + 0.0001
    nMax = nMax - 0.0001
    if oMin == oMax:
        return None
    if nMin == nMax:
        return None
    #check reversed input range
    reverseInput = False
    oldMin = min( oMin, oMax )
    oldMax = max( oMin, oMax )
    if not oldMin == oMin:
        reverseInput = True
    #check reversed output range
    reverseOutput = False   
    newMin = min( nMin, nMax )
    newMax = max( nMin, nMax )
    if not newMin == nMin :
        reverseOutput = True
    portion = (x-oldMin)*(newMax-newMin)/(oldMax-oldMin)
    if reverseInput:
        portion = (oldMax-x)*(newMax-newMin)/(oldMax-oldMin)
    result = portion + newMin
    if reverseOutput:
        result = newMax - portion
    return result




def clamp(value, valueMin, valueMax):
    if value > valueMax :
        return valueMax
    elif value < valueMin:
        return valueMin
    else:
        return value

# This function is deterministic based on noisevalue
def applyUniformNoise(value, noise_level, vtype, paramList= []):
    if noise_level > +1 or noise_level < -1 :
        print("ERROR> STH IS WRONG")
        exit(0)
    if vtype == 'Weather':
        return validWeathers[ int(remap(noise_level, -1, +1, 0, len(validWeathers))) ]
        
    if vtype == 'Model':
        return validModels[ int(remap(noise_level, -1, +1, 0, len(validModels))) ]

    if vtype == 'PlateNumber':
        return validPlateNumbers[ int(remap(noise_level, -1, +1, 0, len(validPlateNumbers))) ]

    if vtype == 'Color':
        return validColors[ int(remap(noise_level, -1, +1, 0, len(validColors))) ]
 
    if vtype == 'BodyType':
        return validBodyType[ int(remap(noise_level, -1, +1, 0, len(validBodyType))) ]

    if vtype == 'Accessory':
        return validAccessories[ int(remap(noise_level, -1, +1, 0, len(validAccessories))) ]
      
    if vtype == 'Gender':
        return validGender[ int(remap(noise_level, -1, +1, 0, len(validGender))) ]          

    print("WARNING> Unknow vtype: ", vtype)
    return value

def applyNumericalNoise(value, noise_value, vtype, valueMin, valueMax):
    if vtype == 'float':
        return clamp(value + noise_value, valueMin, valueMax)
    elif vtype == 'int':
        return int(clamp( value + noise_value, valueMin, valueMax))
    else:
        print("WARNING> Unknow vtype: ", vtype)
        return value
    

# -1 <= noise <= +1
def mutation_function(k, v, noise):
    if noise > 1 and noise < -1 :
        raise Exception("Incorrect noise value:", k , v, noise)
    
    if k == 'X' or k == 'Y' or k == 'Z':
        return applyNumericalNoise(v, noise*10, 'float', -99999, +99999)
    elif k =='Roll' or k=='Pitch' or k=='Yaw' :
        return applyNumericalNoise(v, noise*1, 'float', -99999, +99999)
    elif k=='TargetSpeed':
         return applyNumericalNoise(v, noise*5, 'int', 0, +99999)
    elif k=='AcceptanceRadius':
         return applyNumericalNoise(v, noise*1, 'float', 0, 1)
    elif k=='InitialSpeed':
         return applyNumericalNoise(v, noise*3, 'int', 0, 10)
    elif k=='MaxSpeed':
         return applyNumericalNoise(v, noise*10, 'int', 0, 200)
    elif k=='StartDelay':
         return applyNumericalNoise(v, noise*3, 'int', 0, 10)
    elif k=='Model':
        return applyUniformNoise(v, noise, 'Model' )
    elif k=='Color':
        return applyUniformNoise(v, noise, 'Color')
    elif k=='Gender':
        return applyUniformNoise(v, noise, 'Gender')
    elif k=='BodyType':
        return applyUniformNoise(v, noise, 'BodyType')
    elif k=='Accessory':
        return applyUniformNoise(v, noise, 'Accessory')
    elif k=='PlateNumber':
        return applyUniformNoise(v, noise, 'PlateNumber')
    elif k=='Aperture':
        return applyNumericalNoise(v, noise/10, 'float', 2.7, 2.9)
    elif k=='FocalLength':
        return applyNumericalNoise(v, noise*10, 'int', 0, 10000)
    elif k=='Exposure':
        return applyNumericalNoise(v, noise, 'float', 9, 11)
    elif k=='ShutterSpeed':
        return applyNumericalNoise(v, noise*10, 'int', 0, 500)
    elif k=='Iso':
        return applyNumericalNoise(v, noise*10, 'int', 0, 200)
    elif k=='Fov':
        return applyNumericalNoise(v, noise*2,  'int', 0, 50)
    elif k=='Hour':
        return applyNumericalNoise(v, noise*3, 'int', 0, 24 )
    elif k=='Minute':
        return applyNumericalNoise(v, noise*20, 'int', 0, 60)
    elif k=='Precipitation':
        return applyNumericalNoise(v, noise*1, 'float', 0, 1)
    elif k=='Weather':
        return applyUniformNoise(v, noise, 'Weather')
    else :
        print("Huh, something is missing. No noise schema found for:", k , v, noise)
        return v

"""

    elif k=='Reach':
        return applyNumericalNoise(v, noise*1,  'float', 0, 10000)
    elif k=='HorizontalRange':
        return applyNumericalNoise(v, noise*1, 'float', 0, 100)
    elif k=='VerticalRange':
        return applyNumericalNoise(v, noise*1, 'float', 0, 100)
    elif k=='HorizontalResolution':
        return applyNumericalNoise(v, noise*1, 'float', 0, 100)
    elif k=='VerticalResolution':
        return applyNumericalNoise(v, noise*1, 'float', 0, 2)
"""