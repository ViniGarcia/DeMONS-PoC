import math
import random
import copy

class FlowSimulator:

    __flowsIDs = None

    def __init__(self):
        
        self.__flowsIDs = {'N100/30-1':self.__getFunction_100_0_30_F1,#
                    'N100/30-2':self.__getFunction_100_0_30_F2,#
                    'N500/30':self.__getFunction_500_0_30,#
                    'D500/10':self.__getFunctionDDoS_500_10}

    #==================================== FLOW SOURCE FUNCTIONS ====================================
    def __getFunction_100_0_30_F1(self):
        traffic = []
        for x in range(1,30):
            traffic.append(round(17*math.pow(x,3)/2232 - 1757*math.pow(x,2)/2232 + 6235*x/372, 0) * 1000)
        return traffic

    def __getFunction_100_0_30_F2(self):
        traffic = []
        for x in range(1,30):
            traffic.append(round(66*x/5 - 11*math.pow(x,2)/25, 0) * 1000)
        return traffic

    def __getFunction_500_0_30(self):
        traffic = []
        for x in range(1,30):
            traffic.append(round(135*x/2 - 9*math.pow(x,2)/4, 0) * 1000)
        return traffic

    def __getFunctionDDoS_500_10(self):
        return [500000]*10 + [0]
    #===============================================================================================

    #====================================== FLOW SET FUNCTIONS =====================================
    def __setNormalFlows(self, lastID, lastFlows, targetTraffic):
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


    def __setMaliciousFlows(self, lastID, lastFlows, targetTraffic):
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
    def __createFlowFile(self, traffic, outputName):
        setupTraffic = []
        setupFlows = []
        flowResult = [0, 0, []]

        for i in range(0, len(traffic)):
            flowResult = self.__setNormalFlows(flowResult[0], flowResult[2], traffic[i])
            for flow in flowResult[2]:
                if not 'NA' in flow:
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

    def __createDDoSFile(self, traffic, maliciousTraffic, maliciousTrafficStart, outputName):
        setupTraffic = []
        setupFlows = []
        setupMaliciousTraffic = []
        setupMaliciousFlows = []

        if maliciousTrafficStart + len(maliciousTraffic) > len(traffic):
            return

        flowResult = [0, 0, []]
        for i in range(0, len(traffic)):
            flowResult = self.__setNormalFlows(flowResult[0], flowResult[2], traffic[i])
            for flow in flowResult[2]:
                if not 'NA' in flow:
                    flow.append('NA')
            random.shuffle(flowResult[2])
            setupTraffic.insert(i, flowResult[1])
            setupFlows.insert(i, flowResult[2])

        flowResult = [flowResult[0], 0, []]
        for i in range(0, len(maliciousTraffic)):
            flowResult = self.__setMaliciousFlows(flowResult[0], flowResult[2], maliciousTraffic[i])
            for flow in flowResult[2]:
                if not 'A' in flow:
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

    #======================================== USER FUNCTIONS ========================================

    def flowCreate(self, distribution, file):

        if distribution not in self.__flowsIDs:
            return False

        self.__createFlowFile(self.__flowsIDs[distribution](), file)
        return True

    def ddosCreate(self, benignDistribution, ddosDistribution, ddosStartMoment, file):

        if benignDistribution not in self.__flowsIDs or ddosDistribution not in self.__flowsIDs:
            return False

        if not isinstance(ddosStartMoment, int):
            return False

        self.__createDDoSFile(self.__flowsIDs[benignDistribution](), self.__flowsIDs[ddosDistribution](), ddosStartMoment, file)
        return True

    # ===============================================================================================