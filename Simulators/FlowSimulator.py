import math
import random
import copy

class FlowSimulator:

    __flowsIDs = None

    def __init__(self):
        
        self.__flowsIDs = {'N100/30-1':self.__getFunction_100_0_30_F1,#
                    'N100/30-2':self.__getFunction_100_0_30_F2,#
                    'N500/30':self.__getFunction_500_0_30,#
                    'N1500/30':self.__getFunction_1500_0_30,#
                    'D500/10':self.__getFunctionDDoS_500_10,#
                    'D5000/10':self.__getFunctionDDoS_5000_10,#
                    'P20/40/30':self.__getFunctionRandomPeaks_20_40_30,#
                    'P120/150/30':self.__getFunctionRandomPeaks_120_150_30,#
                    'P200/500/30':self.__getFunctionRandomPeaks_200_500_30,#
                    'I100/30':self.__getFunctionIntermitentPeaks_100_30}

    #==================================== FLOW SOURCE FUNCTIONS ====================================
    def __getFunction_100_0_30_F1(self):
        traffic = []
        for x in range(1,31):
            traffic.append(round(17*math.pow(x,3)/2232 - 1757*math.pow(x,2)/2232 + 6235*x/372, 0) * 1000)
        return traffic

    def __getFunction_100_0_30_F2(self):
        traffic = []
        for x in range(1,31):
            traffic.append(round(66*x/5 - 11*math.pow(x,2)/25, 0) * 1000)
        return traffic

    def __getFunction_500_0_30(self):
        traffic = []
        for x in range(1,31):
            traffic.append(round(135*x/2 - 9*math.pow(x,2)/4, 0) * 1000)
        return traffic

    def __getFunction_1500_0_30(self):
        traffic = []
        for x in range(1,31):
            traffic.append(round(200*x - 20*math.pow(x,2)/3, 0) * 1000)
        return traffic

    def __getFunctionDDoS_500_10(self):
        return [500000]*10 + [0]

    def __getFunctionDDoS_5000_10(self):
        return [5000000]*10 + [0]

    def __getFunctionRandomPeaks_20_40_30(self):
        traffic = []
        for x in range(1,31):
            if random.randint(1,4) != 1:
                traffic.append(0)
            else:
                traffic.append(random.randint(20, 40) * 1000)
        return traffic

    def __getFunctionRandomPeaks_120_150_30(self):
        traffic = []
        for x in range(30):
            if random.randint(1,4) != 1:
                traffic.append(0)
            else:
                traffic.append(random.randint(120, 150) * 1000)
        return traffic

    def __getFunctionRandomPeaks_200_500_30(self):
        traffic = []
        for x in range(30):
            if random.randint(1,4) != 1:
                traffic.append(0)
            else:
                traffic.append(random.randint(200, 500) * 1000)
        return traffic

    def __getFunctionIntermitentPeaks_100_30(self):
        return [1000000 if (i%2) == 1 else 0 for i in range(30)]

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

    def __setPeakFlows(self, lastID, lastFlows, targetTraffic):
        newTraffic = 0
        newFlows = []

        for i in range(0, len(lastFlows)):
            if lastFlows[i][1] != 0:
                if newTraffic < targetTraffic and targetTraffic != 0:
                    copyFlow = copy.copy(lastFlows[i])
                    copyFlow[1] -= 10
                    newTraffic += copyFlow[1]
                    newFlows.append(copyFlow)
                else:
                    copyFlow = copy.copy(lastFlows[i])
                    copyFlow[1] = 0
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
            copyFlow = copy.copy(lastFlows[i])
            if targetTraffic > 0:
                copyFlow[1] = 100
                newFlows.append(copyFlow)
                targetTraffic -= 100
                newTraffic += 100
            else:
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

        output = open(outputName, 'w+')
        for flowHistory in range(0, len(setupTraffic)):
            output.write(str(setupTraffic[flowHistory]) + '\n')
            for flow in setupFlows[flowHistory]:
                output.write(str(flow) + '\n')
            output.write('\n')
        output.close()

        return True

    def __createPeakFile(self, traffic, peakTraffic, outputName):
        setupTraffic = []
        setupFlows = []
        setupPeakTraffic = []
        setupPeakFlows = []

        if len(peakTraffic) > len(traffic):
            return False

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
        for i in range(0, len(peakTraffic)):
            flowResult = self.__setPeakFlows(flowResult[0], flowResult[2], peakTraffic[i])
            for flow in flowResult[2]:
                if not 'NA' in flow:
                    flow.append('NA')
            random.shuffle(flowResult[2])
            setupPeakTraffic.insert(i, flowResult[1])
            setupPeakFlows.insert(i, flowResult[2])

        for i in range(0, len(peakTraffic)):
            setupTraffic[i] += setupPeakTraffic[i]
            setupFlows[i] += setupPeakFlows[i]
            random.shuffle(setupFlows[i])

        output = open(outputName, 'w+')
        for flowHistory in range(0, len(setupTraffic)):
            output.write(str(setupTraffic[flowHistory]) + '\n')
            for flow in setupFlows[flowHistory]:
                output.write(str(flow) + '\n')
            output.write('\n')
        output.close()

        return True

    def __createDDoSFile(self, traffic, maliciousTraffic, maliciousTrafficStart, outputName):
        setupTraffic = []
        setupFlows = []
        setupMaliciousTraffic = []
        setupMaliciousFlows = []

        if maliciousTrafficStart + len(maliciousTraffic) - 1 > len(traffic):
            return False

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

        output = open(outputName, 'w+')
        for flowHistory in range(0, len(setupTraffic)):
            output.write(str(setupTraffic[flowHistory]) + '\n')
            for flow in setupFlows[flowHistory]:
                output.write(str(flow) + '\n')
            output.write('\n')
        output.close()

        return True
    # ===============================================================================================

    #======================================== USER FUNCTIONS ========================================

    def flowCreate(self, distribution, file):

        if distribution not in self.__flowsIDs:
            return False

        return self.__createFlowFile(self.__flowsIDs[distribution](), file)

    def ddosCreate(self, benignDistribution, ddosDistribution, ddosStartMoment, file):

        if benignDistribution not in self.__flowsIDs or ddosDistribution not in self.__flowsIDs:
            return False

        if not isinstance(ddosStartMoment, int):
            return False

        return self.__createDDoSFile(self.__flowsIDs[benignDistribution](), self.__flowsIDs[ddosDistribution](), ddosStartMoment, file)

    def peakCreate(self, benignDistribution, peakDistribution, file):

        if benignDistribution not in self.__flowsIDs or peakDistribution not in self.__flowsIDs:
            return False

        return self.__createPeakFile(self.__flowsIDs[benignDistribution](), self.__flowsIDs[peakDistribution](), file)

    # ===============================================================================================