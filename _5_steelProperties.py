import math

def getBarStress(strain, reinforcementYieldStress):
    if(abs(strain) <= 0.00207):
        barStress = strain * 21000

    elif(strain < - 0.00207):
        barStress = - reinforcementYieldStress / 1.15

    elif(strain > 0.00207):
        barStress = reinforcementYieldStress / 1.15

    return barStress

def getBarProperties(initialStrain, radiusOfCurvature, reinforcementYieldStress, reinforcementBarsList):
    barProperties = [] # [centerPosition, trackStress]

    for i in range(len(reinforcementBarsList)):
        barPosition = reinforcementBarsList[i][1]
        barStrain = initialStrain - radiusOfCurvature * barPosition[1]
        
        barStress = getBarStress(barStrain, reinforcementYieldStress)
        barResultantForce = barStress * (math.pi * 0.25 * (reinforcementBarsList[i][0] / 10) ** 2)

        barProperties.append([barPosition[1], barResultantForce])

    return barProperties
    
def getSteelResultantForce(reinforcementBarsList):
    resultantForce = 0

    for i in range(len(reinforcementBarsList)):
        resultantForce += reinforcementBarsList[i][1]

    return resultantForce

def barsResistantMoment(barProperties, sectionDepth):
    barsResistantMoment = 0

    for i in range(len(barProperties)):
        leverArm = sectionDepth / 2 - barProperties[i][0]
        resistantMoment = leverArm * barProperties[i][1]

        barsResistantMoment += resistantMoment
        
    return barsResistantMoment
