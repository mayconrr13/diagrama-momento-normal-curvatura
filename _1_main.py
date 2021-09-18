from _0_readInputFile import readInputFile
from _2_iteractiveAnalysis import processNormalForceRange
    
(
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
) = readInputFile("inputData.txt")

processNormalForceRange(
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
