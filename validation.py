# Input data - Nsd, teta e dteta, transversal section properties (concrete, steel)
# Units: kN and cm

# Normal, teta and variation
normalForce = 1000
teta = 0.25
maximumError = 10 ** -6
numberOfDivisions = 10

# Section details
sectionWidth = 30
sectionDepth = 30
reinforcementCenterPosition = 4.5 # cover + stirup + 1/2 reiforcement
effectiveDepth = sectionDepth - reinforcementCenterPosition

# Materials details
concreteCompressiveStrength = 4
concreteReducerFactor = 1.4

# relative postion based on the heights point on the section at left. width (X) and depth(Y)
reinforcementBar0 = [16, [4.5, 4.5]]    #diameter, position[x, y]
reinforcementBar1 = [16, [15, 4.5]]
reinforcementBar2 = [16, [25.5, 4.5]]
reinforcementBar3 = [16, [4.5, 15]]
reinforcementBar4 = [16, [25.5, 15]]
reinforcementBar5 = [16, [4.5, 25.5]]
reinforcementBar6 = [16, [15, 25.5]]
reinforcementBar7 = [16, [25.5, 25.5]]

reinforcementsBars = [
    reinforcementBar0,
    reinforcementBar1,
    reinforcementBar2,
    reinforcementBar3,
    reinforcementBar4,
    reinforcementBar5,
    reinforcementBar6,
    reinforcementBar7
]

reinforcementYieldStress = 50
reinforcementReducerFactor = 1.15