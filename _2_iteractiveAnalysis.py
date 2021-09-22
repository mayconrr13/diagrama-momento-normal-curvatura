from _6_resultantMoment import getResultantMoment
from _7_createResultFile import createResultFile, createEnvelopeCurve
from _3_normalStrainIteractiveProcess import resolver

def getThirdCondition(strain, sectionDepth, radiusOfCurvature): 
    condition = strain - radiusOfCurvature * sectionDepth * 0.42867

    return condition

def interactiveProcess(
    normalForce, 
    maximumError, 
    sectionDepth, 
    reinforcementCenterPosition, 
    teta, 
    initialStrain, 
    limitStress, 
    sectionWidth, 
    numberOfDivisions, 
    reinforcementBars, 
    concreteCompressiveStrength, 
    reinforcementYieldStress
):
    processResults = []

    effectiveDepth = sectionDepth - reinforcementCenterPosition
    strain = initialStrain
    teta = teta
    radiusOfCurvature = teta / (1000 * effectiveDepth)
    condition = 0

    while strain <= 0.0035 and condition <= 0.002:
        trackProperties, barProperties, strain = resolver(
            normalForce, 
            maximumError, 
            strain, 
            radiusOfCurvature, 
            limitStress, 
            sectionWidth, 
            sectionDepth, 
            numberOfDivisions, 
            reinforcementBars, 
            concreteCompressiveStrength, 
            reinforcementYieldStress
        )

        strain = strain
        condition = getThirdCondition(strain, sectionDepth, radiusOfCurvature) 

        if(strain > 0.0035 or condition > 0.002):
            break       

        resultantMoment = getResultantMoment(trackProperties, barProperties, sectionDepth)

        processResults.append([normalForce, teta, resultantMoment])

        teta += 0.1
        radiusOfCurvature = teta / (1000 * effectiveDepth)

    return processResults

def getResultsPerNormalForceLevel(
    normalForceInitial, 
    sectionDepth, 
    reinforcementCenterPosition, 
    sectionWidth, 
    numberOfDivisions, 
    reinforcementBars, 
    concreteCompressiveStrength, 
    reinforcementYieldStress
):

    limitStress = ['85', '110']
    normalForce = normalForceInitial
    resistantMoment = []

    for i in range(len(limitStress)):
        results = interactiveProcess(
            normalForce, 
            10 ** -6, 
            sectionDepth, 
            reinforcementCenterPosition, 
            0.1, 
            0.002, 
            limitStress[i],
            sectionWidth, 
            numberOfDivisions, 
            reinforcementBars, 
            concreteCompressiveStrength, 
            reinforcementYieldStress
        )

        if(len(results) == 0):
            print("Força normal de " + str(normalForce) + " fora dos limites!")
            return False, []

        createResultFile(limitStress[i], results)

        if(i == 0):
            resistantMoment = results[-1]
            
    print("Processo finalizado para força normal " + str(normalForce) + "!")
    return True, resistantMoment

def processNormalForceRange(
        sectionWidth, 
        sectionDepth, 
        reinforcementCenterPosition, 
        concreteCompressiveStrength, 
        reinforcementYieldStress, 
        normalForceInitial,
        normalForceVariation,
        normalForceLimit,
        numberOfDivisions,
        reinforcementBars
    ):
    
    normalForce = normalForceInitial
    envelopeCurvePoints = []

    while (normalForce <= normalForceLimit):
        hasResults, momentResistant = getResultsPerNormalForceLevel(
            normalForce, 
            sectionDepth, 
            reinforcementCenterPosition, 
            sectionWidth, 
            numberOfDivisions, 
            reinforcementBars, 
            concreteCompressiveStrength, 
            reinforcementYieldStress
        )

        if(hasResults == False):
            break
        
        if(len(momentResistant) > 0):
            envelopeCurvePoints.append([normalForce, momentResistant[2]])

        normalForce += normalForceVariation

    createEnvelopeCurve(envelopeCurvePoints)

    print("Envoltória criada")
    print("--- END ---")
    return
