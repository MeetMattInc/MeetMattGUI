import numpy as np
import scipy.ndimage as ndimage
import math

#print("running...")

def getDiagonalAndArea(pMap, binaryErosion = True):
    npArray = np.array(pMap)

    if binaryErosion:
        npArray = ndimage.morphology.binaryErosion(npArray)

    objectsFound = ndimage.measurements.find_objects(npArray)
    
    if len(objectsFound) == 0:
        return (0, 0)

    maxDiag = 0
    objectForMaxDaig = None
    areaForMaxDiag = 0
    
    for objectFound in objectsFound:
        xmin = objectFound[0].start
        xmax = objectFound[0].stop
  
        ymin = objectFound[1].start
        ymax = objectFound[1].stop
                          
        diag = math.sqrt((xmax-xmin)**2 + (ymax-ymin)**2) 
        
        if diag > maxDiag:
            maxDiag = diag
            objectForMaxDaig = objectFound
    
    areaForMaxDiag = np.count_nonzero(npArray[objectForMaxDaig])
    
    return (maxDiag, areaForMaxDiag)
