from _4_concreteProperties import getConcreteTrackProperties, getConcreteResultantForce
from _5_steelProperties import getBarProperties, getSteelResultantForce

def getCorrectionFactor(normalForce):
    if(normalForce < 300):
        return 0.01
    if(normalForce >= 300 and normalForce < 600):
        return 0.1
    elif(normalForce >= 600 and normalForce < 800):
        return 0.2
    else:
        return 0.5

def updateStrain(strain, previousError, normalForce):
    correctionFactor = getCorrectionFactor(normalForce)

    updatedStrain = strain * (1 + correctionFactor * previousError / normalForce)

    return updatedStrain

def resolver(
    normalForce, 
    maximumError, 
    strain, 
    radiusOfCurvature, 
    limitStress, sectionWidth, 
    sectionDepth, 
    numberOfDivisions, 
    reinforcementBars, 
    concreteCompressiveStrength, 
    reinforcementYieldStress
):
    barResultant = 0
    concreteResultant = 0

    error = 1
    radiusOfCurvature = radiusOfCurvature
    strain = strain
    numberOfIterations = 0    

    while (abs(error) > maximumError):
        trackProperties = getConcreteTrackProperties(sectionWidth, sectionDepth, numberOfDivisions, strain, radiusOfCurvature, concreteCompressiveStrength, limitStress)
        concreteResultant = getConcreteResultantForce(trackProperties)

        barProperties = getBarProperties(strain, radiusOfCurvature, reinforcementYieldStress, reinforcementBars)
        barResultant = getSteelResultantForce(barProperties)

        error = normalForce - (barResultant + concreteResultant) 
        strain = updateStrain(strain, error, normalForce)  
        numberOfIterations += 1

        if(strain > 0.0035 or numberOfIterations > 1000):
            break   

    return trackProperties, barProperties, strain
