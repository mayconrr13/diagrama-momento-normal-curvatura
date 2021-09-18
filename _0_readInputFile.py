def lineToIgnore(inputFile: str):
    inputFile.readline()
    return

def readInputFile(file: str):
    inputFile = open(file, "r")

    lineToIgnore(inputFile)

    sectionWidth = int(inputFile.readline().split("=")[1])
    sectionDepth = int(inputFile.readline().split("=")[1])
    reinforcementCenterPosition = float(inputFile.readline().split("=")[1])
    numberOfBars = int(inputFile.readline().split("=")[1])

    lineToIgnore(inputFile)
    lineToIgnore(inputFile)

    concreteCompressiveStrength = int(inputFile.readline().split("=")[1])
    reinforcementYieldStress = int(inputFile.readline().split("=")[1])

    lineToIgnore(inputFile)
    lineToIgnore(inputFile)

    normalForceInitial = int(inputFile.readline().split("=")[1])
    normalForceLimit = int(inputFile.readline().split("=")[1])
    normalForceVariation = int(inputFile.readline().split("=")[1])
    numberOfDivisions = int(inputFile.readline().split("=")[1])

    lineToIgnore(inputFile)
    lineToIgnore(inputFile)
    lineToIgnore(inputFile)

    reinforcementBars = []

    for i in range(numberOfBars):
        barProperties = inputFile.readline().split(",")
        reinforcementBars.append([float(barProperties[1]), [float(barProperties[2]), float(barProperties[3])]])

    inputFile.close()

    return (
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
    )