import math

# Input data - Nsd, teta e dteta, transversal section properties (concrete, steel)
# Units: kN and cm

# Normal, teta and variation
normalForce = 1000
teta = 0.1
maximumError = 10 ** -8
numberOfDivisions = 20

# Section details
sectionWidth = 40
sectionDepth = 20
reinforcementCenterPosition = 4 # cover + stirup + 1/2 reiforcement
effectiveDepth = sectionDepth - reinforcementCenterPosition

# Materials details
concreteCompressiveStrength = 3
concreteReducerFactor = 1.4

# relative postion based on the heights point on the section at left. width (X) and depth(Y)
reinforcementBar0 = [16, [4, 4]]    #diameter, position[x, y]
reinforcementBar1 = [16, [20, 4]]
reinforcementBar2 = [16, [36, 4]]
reinforcementBar3 = [16, [4, 16]]
reinforcementBar4 = [16, [20, 16]]
reinforcementBar5 = [16, [36, 16]]

reinforcementsBars = [
    reinforcementBar0,
    reinforcementBar1,
    reinforcementBar2,
    reinforcementBar3,
    reinforcementBar4,
    reinforcementBar5
]

reinforcementYieldStress = 50
reinforcementReducerFactor = 1.15

def getConcreteTrackStress(strain, concreteCompressiveStrength):
    if(strain <= 0):
       trackStress = 0

    elif(strain < 0.002):
        trackStress = 0.85 * (concreteCompressiveStrength / 1.4) * (1 - (1 - strain / 0.002) ** 2)

    else:
        trackStress = 0.85 * (concreteCompressiveStrength / 1.4)
    
    return trackStress

def getConcreteTrackProperties(sectionWidth, sectionDepth, numberOfDivisions, initialStrain, radiusOfCurvature, concreteCompressiveStrength):
    concreteTracksWidth = sectionDepth / numberOfDivisions

    trackProperties = [] # [centerPosition, trackResultantForce]

    for i in range(numberOfDivisions):
        centerPosition = concreteTracksWidth * (i) + concreteTracksWidth / 2
        trackStrain = initialStrain - radiusOfCurvature * centerPosition
        trackStress = getConcreteTrackStress(trackStrain, concreteCompressiveStrength)
        trackResultantForce = trackStress * (concreteTracksWidth * sectionWidth)

        trackProperties.append([centerPosition, trackResultantForce])

    return trackProperties
    
def getConcreteResultantForce(concreteTracksStressList):        
    resultantForce = 0

    for i in range(len(concreteTracksStressList)):
        resultantForce += concreteTracksStressList[i][1]

    return resultantForce

def getBarStress(strain, reinforcementYieldStress):
    if(abs(strain) <= 0.00207):
        barStress = strain * 21000

    elif(strain < - 0.00207):
        barStress = - reinforcementYieldStress / 1.15

    elif(strain > 0.00207):
        barStress = reinforcementYieldStress / 1.15

    return barStress

def getBarProperties(initialStrain, radiusOfCurvature, reinforcementYieldStress, reinforcementsBarsList):
    barProperties = [] # [centerPosition, trackStress]

    for i in range(len(reinforcementsBarsList)):
        barPosition = reinforcementsBarsList[i][1]
        barStrain = initialStrain - radiusOfCurvature * barPosition[1]
        # print(barStrain)
        barStress = getBarStress(barStrain, reinforcementYieldStress)
        barResultantForce = barStress * (math.pi * 0.25 * (reinforcementsBarsList[i][0] / 10) ** 2)

        barProperties.append([barPosition[1], barResultantForce])

    return barProperties
    
def getSteelResultantForce(reinforcementsBarsList):
    resultantForce = 0

    for i in range(len(reinforcementsBarsList)):
        resultantForce += reinforcementsBarsList[i][1]

    return resultantForce

def updateStrain(strain, previousError, normalForce):
    updatedStrain = strain * (1 + 0.5 * (- previousError / normalForce))

    return updatedStrain

def resolver(normalForce, maximumError, strain, radiusOfCurvature):
    barResultant = 0
    concreteResultant = 0

    error = 1
    radiusOfCurvature = radiusOfCurvature
    strain = strain

    while (abs(error) > maximumError):
        trackProperties = getConcreteTrackProperties(sectionWidth, sectionDepth, numberOfDivisions, strain, radiusOfCurvature, concreteCompressiveStrength)
        concreteResultant = getConcreteResultantForce(trackProperties)

        barProperties = getBarProperties(strain, radiusOfCurvature, reinforcementYieldStress, reinforcementsBars)
        barResultant = getSteelResultantForce(barProperties)

        error = (barResultant + concreteResultant) - normalForce
        strain = updateStrain(strain, error, normalForce)     

    return trackProperties, barProperties, strain

def tracksResistantMoment(trackProperties, sectionDepth):
    tracksResistantMoment = 0

    for i in range(len(trackProperties)):
        leverArm = sectionDepth / 2 - trackProperties[i][0]
        resistantMoment = leverArm * trackProperties[i][1]
        
        tracksResistantMoment += resistantMoment
    
    return tracksResistantMoment

def barsResistantMoment(barProperties, sectionDepth):
    barsResistantMoment = 0

    for i in range(len(barProperties)):
        leverArm = sectionDepth / 2 - barProperties[i][0]
        resistantMoment = leverArm * barProperties[i][1]

        barsResistantMoment += resistantMoment
        
    return barsResistantMoment

def getResultantMoment(trackProperties, barProperties, sectionDepth):
    concreteTracksResultant = tracksResistantMoment(trackProperties, sectionDepth)
    reinfocementBarsResultant = barsResistantMoment(barProperties, sectionDepth)

    resultantMoment = concreteTracksResultant + reinfocementBarsResultant

    return resultantMoment

def interactiveProcess(normalForce, maximumError, sectionDepth, teta, initialStrain):
    processResults = []

    check = initialStrain
    teta = teta
    radiusOfCurvature = teta / (1000 * effectiveDepth)

    while (check < 0.0035):
        trackProperties, barProperties, strain = resolver(normalForce, maximumError, check, radiusOfCurvature)
        check = strain

        resultantMoment = getResultantMoment(trackProperties, barProperties, sectionDepth)

        processResults.append([normalForce, teta, resultantMoment])
        teta += 0.1
        radiusOfCurvature = teta / (1000 * effectiveDepth)

    else:
        print("Processo encerrado para esse nível de força normal.")

    return processResults

results = interactiveProcess(normalForce, maximumError, sectionDepth, teta, 0.002)
print(results)