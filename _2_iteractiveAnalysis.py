from _6_resultantMoment import getResultantMoment
from _7_createResultFile import createResultFile
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
    check = initialStrain
    teta = teta
    radiusOfCurvature = teta / (1000 * effectiveDepth)

    while (check < 0.0035):
        trackProperties, barProperties, strain = resolver(
            normalForce, 
            maximumError, 
            check, 
            radiusOfCurvature, 
            limitStress, 
            sectionWidth, 
            sectionDepth, 
            numberOfDivisions, 
            reinforcementBars, 
            concreteCompressiveStrength, 
            reinforcementYieldStress
        )

        check = strain

        resultantMoment = getResultantMoment(trackProperties, barProperties, sectionDepth)

        processResults.append([normalForce, teta, resultantMoment])

        condition = getThirdCondition(strain, sectionDepth, radiusOfCurvature)
        if(condition >= 0.002):
            break
        
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

        createResultFile(limitStress[i], results)

    print("Processo finalizado para força normal " + str(normalForce) + "!")

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

    while (normalForce <= normalForceLimit):
        getResultsPerNormalForceLevel(
            normalForce, 
            sectionDepth, 
            reinforcementCenterPosition, 
            sectionWidth, 
            numberOfDivisions, 
            reinforcementBars, 
            concreteCompressiveStrength, 
            reinforcementYieldStress
        )

        normalForce += normalForceVariation

    print("--- END ---")
    return
