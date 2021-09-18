def getConcreteTrackStress(strain, concreteCompressiveStrength, limitStress):
    coefficients = {
        "85": 0.85,
        "110": 1.1,
    }

    if(strain <= 0):
       trackStress = 0

    elif(strain < 0.002):
        trackStress = coefficients[limitStress] * (concreteCompressiveStrength / 1.4) * (1 - (1 - strain / 0.002) ** 2)

    else:
        trackStress = coefficients[limitStress] * (concreteCompressiveStrength / 1.4)
    
    return trackStress

def getConcreteTrackProperties(sectionWidth, sectionDepth, numberOfDivisions, initialStrain, radiusOfCurvature, concreteCompressiveStrength, limitStress):
    concreteTracksWidth = sectionDepth / numberOfDivisions

    trackProperties = [] # [centerPosition, trackResultantForce]

    for i in range(numberOfDivisions):
        centerPosition = concreteTracksWidth * (i) + concreteTracksWidth / 2
        trackStrain = initialStrain - radiusOfCurvature * centerPosition
        trackStress = getConcreteTrackStress(trackStrain, concreteCompressiveStrength, limitStress)
        trackResultantForce = trackStress * (concreteTracksWidth * sectionWidth)

        trackProperties.append([centerPosition, trackResultantForce])

    return trackProperties
    
def getConcreteResultantForce(concreteTracksStressList):        
    resultantForce = 0

    for i in range(len(concreteTracksStressList)):
        resultantForce += concreteTracksStressList[i][1]

    return resultantForce

def tracksResistantMoment(trackProperties, sectionDepth):
    tracksResistantMoment = 0

    for i in range(len(trackProperties)):
        leverArm = sectionDepth / 2 - trackProperties[i][0]
        resistantMoment = leverArm * trackProperties[i][1]
        
        tracksResistantMoment += resistantMoment
    
    return tracksResistantMoment

