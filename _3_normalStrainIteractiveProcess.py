from _4_concreteProperties import getConcreteTrackProperties, getConcreteResultantForce
from _5_steelProperties import getBarProperties, getSteelResultantForce

def getCorrectionFactor(normalForce):
    if(normalForce < 1000):
        return 0.02

    else:
        return 0.2

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

    while (abs(error) > maximumError) and (numberOfIterations <= 1000):
        trackProperties = getConcreteTrackProperties(sectionWidth, sectionDepth, numberOfDivisions, strain, radiusOfCurvature, concreteCompressiveStrength, limitStress)
        concreteResultant = getConcreteResultantForce(trackProperties)

        barProperties = getBarProperties(strain, radiusOfCurvature, reinforcementYieldStress, reinforcementBars)
        barResultant = getSteelResultantForce(barProperties)

        error = normalForce - (barResultant + concreteResultant) 
        strain = updateStrain(strain, error, normalForce)       
        numberOfIterations += 1       

    return trackProperties, barProperties, strain
