from _6_resultantMoment import getResultantMoment
from _7_createResultFile import createResultFile, createEnvelopeCurve
from _3_normalStrainIteractiveProcess import resolver

def checkSectionDomain(strain, sectionDepth, radiusOfCurvature): 
    condition = strain - radiusOfCurvature * sectionDepth * 0.42867

    return condition

def checkBarStrain(barPropertiesList):
    barStrain = []

    for i in range(len(barPropertiesList)):
        strain = abs(barPropertiesList[i][2])
        barStrain.append(strain)

    maximumStrain = max(barStrain)

    return maximumStrain

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
    teta = teta
    radiusOfCurvature = teta / (1000 * effectiveDepth)
    
    concreteStrain = initialStrain
    barMaximumStrain = 0
    fifthDomain = 0

    while concreteStrain <= 0.0035 and barMaximumStrain <= 0.01 and fifthDomain <= 0.002:
        trackProperties, barProperties, strain = resolver(
            normalForce, 
            maximumError, 
            concreteStrain, 
            radiusOfCurvature, 
            limitStress, 
            sectionWidth, 
            sectionDepth, 
            numberOfDivisions, 
            reinforcementBars, 
            concreteCompressiveStrength, 
            reinforcementYieldStress
        )

        concreteStrain = strain
        barMaximumStrain = checkBarStrain(barProperties)
        fifthDomain = checkSectionDomain(concreteStrain, sectionDepth, radiusOfCurvature) 

        if(concreteStrain > 0.0035 or barMaximumStrain > 0.01 or fifthDomain > 0.002):
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
    firstSituationProceed = True
    secondSituationProceed = True

    for i in range(len(limitStress)):
        results = interactiveProcess(
            normalForce, 
            10 ** -8, 
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

        if(len(results) == 0 and i == 0):
            print("Força normal de " + str(normalForce) + " fora dos limites (0.85fcd)!")
            firstSituationProceed = False

        elif(len(results) == 0 and i == 1):
            print("Força normal de " + str(normalForce) + " fora dos limites (1.10fcd)!")
            secondSituationProceed = False
        
        else:
            createResultFile(limitStress[i], results)

            if(i == 0):
                resistantMoment = results[-1]

        if(firstSituationProceed == False and secondSituationProceed == False):
            print("Processo interrompido por se encontrar fora de ambos limites")
            return False, []
            
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
