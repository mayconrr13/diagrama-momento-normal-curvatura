import math

# Input data - Nsd, teta e dteta, transversal section properties (concrete, steel)
# Units: kN and cm

# Normal, teta and variation
normalForceInitial = 900
normalForceVariation = 50
normalForceLimit = 1100
teta = 0.1
maximumError = 10 ** -6
numberOfDivisions = 10

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
    updatedStrain = abs(strain * (1 - 0.5 * previousError / normalForce))
    
    return updatedStrain

def resolver(normalForce, maximumError, strain, radiusOfCurvature, limitStress):
    barResultant = 0
    concreteResultant = 0

    error = 1
    radiusOfCurvature = radiusOfCurvature
    strain = strain

    while (abs(error) > maximumError):
        trackProperties = getConcreteTrackProperties(sectionWidth, sectionDepth, numberOfDivisions, strain, radiusOfCurvature, concreteCompressiveStrength, limitStress)
        concreteResultant = getConcreteResultantForce(trackProperties)

        barProperties = getBarProperties(strain, radiusOfCurvature, reinforcementYieldStress, reinforcementsBars)
        barResultant = getSteelResultantForce(barProperties)

        error = (barResultant + concreteResultant) - normalForce
        strain = updateStrain(strain, error, normalForce)  

        if(strain > 0.0035):
            break   

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

def interactiveProcess(normalForce, maximumError, sectionDepth, teta, initialStrain, limitStress):
    processResults = []

    check = initialStrain
    teta = teta
    radiusOfCurvature = teta / (1000 * effectiveDepth)

    while (check < 0.0035):
        trackProperties, barProperties, strain = resolver(normalForce, maximumError, check, radiusOfCurvature, limitStress)
        check = strain

        resultantMoment = getResultantMoment(trackProperties, barProperties, sectionDepth)

        processResults.append([normalForce, teta, resultantMoment])
        teta += 0.1
        radiusOfCurvature = teta / (1000 * effectiveDepth)

    return processResults

def createResultFile(limitStress, results):
    file = open('N' + str(results[0][0]) + '_' + limitStress + '.txt', "a")

    file.write('Normal Force: ' + str(results[0][0]) + '\n')
    file.write('Concrete stress: ' + str(limitStress) + '\n\n')
    file.write('θ, Mrd\n' )

    for j in range(len(results)):
        file.write('%.1f' % results[j][1] + ', ' + str(results[j][2]) + '\n')

    file.close()

def getResultsPerNormalForceLevel(normalForceInitial, sectionDepth):
    limitStress = ['85', '110']
    normalForce = normalForceInitial

    for i in range(len(limitStress)):
        results = interactiveProcess(normalForce, 10 ** -8, sectionDepth, 0.1, 0.002, limitStress[i])

        createResultFile(limitStress[i], results)

    print("Processo finalizado para força normal " + str(normalForce) + "!")

def processNormalForceRange(normalForceInitial, normalForceVariation):
    normalForce = normalForceInitial

    while (normalForce <= normalForceLimit):
        getResultsPerNormalForceLevel(normalForce, sectionDepth)
        normalForce += normalForceVariation

    print("--- END ---")
    return

processNormalForceRange(normalForceInitial, normalForceVariation)