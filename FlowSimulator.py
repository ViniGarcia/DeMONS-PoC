import math
import random
import copy

#==================================== FLOW SOURCE FUNCTIONS ====================================
def getFunction_100_0_30_F1():
    traffic = []
    for x in range(1,30):
        traffic.append(round(17*math.pow(x,3)/2232 - 1757*math.pow(x,2)/2232 + 6235*x/372, 0) * 1000)
    return traffic

def getFunction_100_0_30_F2():
    traffic = []
    for x in range(1,30):
        traffic.append(round(66*x/5 - 11*math.pow(x,2)/25, 0) * 1000)
    return traffic

def getFunction_500_0_30():
    traffic = []
    for x in range(1,30):
        traffic.append(round(135*x/2 - 9*math.pow(x,2)/4, 0) * 1000)
    return traffic

def getFunctionDDoS_500_10():
    return [500000]*10 + [0]
#===============================================================================================

#====================================== FLOW SET FUNCTIONS =====================================
def setNormalFlows(lastID, lastFlows, targetTraffic):
    newTraffic = 0
    newFlows = []

    for i in range(0, len(lastFlows)):
        if lastFlows[i][1] != 0:
            copyFlow = copy.copy(lastFlows[i])
            copyFlow[1] -= 10
            newTraffic += copyFlow[1]
            newFlows.append(copyFlow)

    remainingTraffic = targetTraffic - newTraffic
    while remainingTraffic > 0:
        lastID += 1
        newTraffic += 100
        remainingTraffic -= 100
        newFlows.append([lastID, 100, random.randint(4,10)/10])

    return [lastID, newTraffic, newFlows]


def setMaliciousFlows(lastID, lastFlows, targetTraffic):
    newTraffic = 0
    newFlows = []

    for i in range(0, len(lastFlows)):
        if targetTraffic != 0:
            return [lastID, targetTraffic, lastFlows]
        else:
            copyFlow = copy.copy(lastFlows[i])
            copyFlow[1] = 0
            newFlows.append(copyFlow)

    while targetTraffic > 0:
        lastID += 1
        newTraffic += 100
        targetTraffic -= 100
        newFlows.append([lastID, 100, random.randint(1,4)/10])


    return [lastID, newTraffic, newFlows]
#===============================================================================================

#==================================== FLOW CREATE FUNCTIONS ====================================
def createFlowFile(traffic, outputName):
    setupTraffic = []
    setupFlows = []
    flowResult = [0, 0, []]

    for i in range(0, len(traffic)):
        flowResult = setNormalFlows(flowResult[0], flowResult[2], traffic[i])
        for flow in flowResult[2]:
            flow.append('NA')
        random.shuffle(flowResult[2])
        setupTraffic.insert(i, flowResult[1])
        setupFlows.insert(i, flowResult[2])

    output = open(outputName, 'w')
    for flowHistory in range(0, len(setupTraffic)):
        output.write(str(setupTraffic[flowHistory]) + '\n')
        for flow in setupFlows[flowHistory]:
            output.write(str(flow) + '\n')
        output.write('\n')

def createDDoSFile(traffic, maliciousTraffic, maliciousTrafficStart, outputName):
    setupTraffic = []
    setupFlows = []
    setupMaliciousTraffic = []
    setupMaliciousFlows = []

    if maliciousTrafficStart + len(maliciousTraffic) > len(traffic):
        return

    flowResult = [0, 0, []]
    for i in range(0, len(traffic)):
        flowResult = setNormalFlows(flowResult[0], flowResult[2], traffic[i])
        for flow in flowResult[2]:
            flow.append('NA')
        random.shuffle(flowResult[2])
        setupTraffic.insert(i, flowResult[1])
        setupFlows.insert(i, flowResult[2])

    flowResult = [flowResult[0], 0, []]
    for i in range(0, len(maliciousTraffic)):
        flowResult = setMaliciousFlows(flowResult[0], flowResult[2], maliciousTraffic[i])
        for flow in flowResult[2]:
            flow.append('A')
        random.shuffle(flowResult[2])
        setupMaliciousTraffic.insert(i, flowResult[1])
        setupMaliciousFlows.insert(i, flowResult[2])

    for i in range(maliciousTrafficStart - 1, maliciousTrafficStart + len(maliciousTraffic) - 1):
        setupTraffic[i] += setupMaliciousTraffic[i-maliciousTrafficStart + 1]
        setupFlows[i] += setupMaliciousFlows[i-maliciousTrafficStart + 1]
        random.shuffle(setupFlows[i])

    output = open(outputName, 'w')
    for flowHistory in range(0, len(setupTraffic)):
        output.write(str(setupTraffic[flowHistory]) + '\n')
        for flow in setupFlows[flowHistory]:
            output.write(str(flow) + '\n')
        output.write('\n')
# ===============================================================================================

#createFlowFile(getFunction_100_0_30_F2(), 'Traffic100_0_30_F2.txt')
#createDDoSFile(getFunction_100_0_30_F2(), getFunctionDDoS_500_10(), 10, 'DDoS_100_30_F2_500_10_2.txt')