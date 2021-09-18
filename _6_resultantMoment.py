from _4_concreteProperties import tracksResistantMoment
from _5_steelProperties import barsResistantMoment

def getResultantMoment(trackProperties, barProperties, sectionDepth):
    concreteTracksResultant = tracksResistantMoment(trackProperties, sectionDepth)
    reinfocementBarsResultant = barsResistantMoment(barProperties, sectionDepth)

    resultantMoment = concreteTracksResultant + reinfocementBarsResultant

    return resultantMoment