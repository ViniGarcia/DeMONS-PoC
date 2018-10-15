from sys import path
from math import pow

path.insert(0, '../Solutions/')
from VGuard import VGuard
from DeMONS import DeMONS

class MethodsSimulator:

    def trafficHistoryInsert(self, flowID, flowPriority, flowIntensity, flowType, testMethod):
        for flow in testMethod.tunnelHighFlows:
            if flow[2] == flowID:
                if flowIntensity == 0:
                    testMethod.tunnelHighUse -= flow[1]
                    testMethod.tunnelHighSum -= flow[0]
                    testMethod.tunnelHighFlows.remove(flow)
                else:
                    if flowIntensity != flow[1]:
                        testMethod.tunnelHighUse += flowIntensity - flow[1]
                        flow[1] = flowIntensity
                    if flowPriority != flow[0]:
                        testMethod.tunnelHighSum += flowPriority - flow[0]
                        flow[0] = flowPriority
                return
        for flow in testMethod.tunnelLowFlows:
            if flow[2] == flowID:
                if flowIntensity == 0:
                    testMethod.tunnelLowUse -= flow[1]
                    testMethod.tunnelLowSum -= flow[0]
                    testMethod.tunnelLowFlows.remove(flow)
                else:
                    if flowIntensity != flow[1]:
                        testMethod.tunnelLowUse += flowIntensity - flow[1]
                        flow[1] = flowIntensity
                    if flowPriority != flow[0]:
                        testMethod.tunnelLowSum += flowPriority - flow[0]
                        flow[0] = flowPriority
                return

        if isinstance(testMethod, DeMONS):
            testMethod.selectiveFlowAllocation(flowID, flowPriority, flowIntensity, flowType)
        else:
            if isinstance(testMethod, VGuard):
                testMethod.flowAllocation(flowID, flowPriority, flowIntensity, flowType)


    def lowTunnelSatisfaction(self, testMethod):
        dropRate = 1 - min(1, testMethod.tunnelLowCapacity/testMethod.tunnelLowUse)
        satisfaction = pow((1 - dropRate),2)
        maxSatisfaction = 0
        currentSatisfaction = 0

        for flow in testMethod.tunnelLowFlows:
            currentSatisfaction += flow[1] * flow[0] * satisfaction
            maxSatisfaction += flow[1] * flow[0]

        return [currentSatisfaction, maxSatisfaction]


    def lowFilteredTunnelSatisfaction(self, testMethod):
        dropRate = 1 - min(1, testMethod.tunnelLowCapacity/(testMethod.tunnelLowUse - testMethod.tunnelLowDropRate))
        satisfaction = pow((1 - dropRate),2)
        maxSatisfaction = 0
        currentSatisfaction = 0

        for flow in testMethod.tunnelLowFlows:
            if flow[2] in testMethod.tunnelLowDrop:
                filterFlowDrop = testMethod.tunnelLowDrop[flow[2]]
                tunnelFlowDrop = (flow[1] - testMethod.tunnelLowDrop[flow[2]]) * dropRate
                flowDropRate = (filterFlowDrop + tunnelFlowDrop)/flow[1]
                flowSatisfaction = pow((1 - flowDropRate), 2)
                currentSatisfaction += flow[1] * flow[0] * flowSatisfaction
            else:
                currentSatisfaction += flow[1] * flow[0] * satisfaction
            maxSatisfaction += flow[1] * flow[0]

        return [currentSatisfaction, maxSatisfaction]


    def highTunnelSatisfaction(self, testMethod):
        dropRate = 1 - min(1, testMethod.tunnelHighCapacity/testMethod.tunnelHighUse)
        satisfaction = pow((1 - dropRate),2)
        maxSatisfaction = 0
        currentSatisfaction = 0

        for flow in testMethod.tunnelHighFlows:
            currentSatisfaction += flow[1] * flow[0] * satisfaction
            maxSatisfaction += flow[1] * flow[0]

        return [currentSatisfaction, maxSatisfaction]


    def generateBasicReport(self, testMethod):
        lowSatisfaction = self.lowTunnelSatisfaction(testMethod)
        lowFilteredSatisfaction = self.lowFilteredTunnelSatisfaction(testMethod)
        highSatisfaction = self.highTunnelSatisfaction(testMethod)

        print('====================== BASIC REPORT ======================')
        print('Low Tunnel Flows Amount: ' + str(len(testMethod.tunnelLowFlows)))
        print('Low Tunnel Flows Priority Sum: ' + str(testMethod.tunnelLowSum))
        print('Low Tunnel Crossing Traffic: ' + str(testMethod.tunnelLowUse))
        print('Low Tunnel Current Satisfaction: ' + str(lowSatisfaction[0]))
        print('Low Tunnel Filtered Satisfaction: ' + str(lowFilteredSatisfaction[0]))
        print('Low Tunnel Filtered Maximum Satisfaction: ' + str(lowFilteredSatisfaction[1]))
        print('Low Tunnel Maximum Satisfaction: ' + str(lowSatisfaction[1]))
        print('High Tunnel Flows Amount: ' + str(len(testMethod.tunnelHighFlows)))
        print('High Tunnel Flows Priority Sum: ' + str(testMethod.tunnelHighSum))
        print('High Tunnel Crossing Traffic: ' + str(testMethod.tunnelHighUse))
        print('High Tunnel Current Satisfaction: ' + str(highSatisfaction[0]))
        print('High Tunnel Maximum Satisfaction: ' + str(highSatisfaction[1]))
        print('==========================================================')

    def generateFilterReport(self, testMethod):
        priorities = [0]*10
        traffic = [0]*10

        for flow in testMethod.tunnelLowFlows:
            priorities[int(flow[0]*10)-1] += 1
            traffic[int(flow[0]*10)-1] += flow[1]

        print('====================== FILTER REPORT ======================')
        for index in range(0,10):
            print('Priority: ' + str(index+1) + ' Flow Amount: ' + str(priorities[index]) + ' Traffic: ' + str(traffic[index]))
        print('Filter Drop Rate: ' + str(testMethod.tunnelLowDropRate))
        print('After Filter Traffic: ' + str(testMethod.tunnelLowUse - testMethod.tunnelLowDropRate))
        print('After Filter Tunnel Drop Rate: ' + str((testMethod.tunnelLowUse - testMethod.tunnelLowDropRate)/len(testMethod.tunnelLowFlows)))
        print('==========================================================')

    def generateDDoSReport(self, testMethod):
        benignLowPassRate = 0
        benignHighPassRate = 0
        filteredBenignLowPassRate = 0
        benignLowTraffic = 0
        benignHighTraffic = 0
        tunnelLowAtacks = 0
        tunnelLowAtackTraffic = 0
        tunnelHighAtacks = 0
        tunnelHighAttackTraffic = 0

        passRate = min(1, testMethod.tunnelLowCapacity / testMethod.tunnelLowUse)
        filteredPassRate = min(1, testMethod.tunnelLowCapacity / (testMethod.tunnelLowUse - testMethod.tunnelLowDropRate))

        for flow in testMethod.tunnelLowFlows:
            if flow[3] == '\'A\'':
                tunnelLowAtacks += 1
                tunnelLowAtackTraffic += flow[1]
            else:
                benignLowPassRate += flow[1] * passRate
                if flow[2] in testMethod.tunnelLowDrop:
                    filteredBenignLowPassRate += (flow[1] - testMethod.tunnelLowDrop[flow[2]]) * filteredPassRate
                else:
                    filteredBenignLowPassRate += flow[1] * filteredPassRate
                benignLowTraffic += flow[1]

        passRate = min(1, testMethod.tunnelHighCapacity / testMethod.tunnelHighUse)
        for flow in testMethod.tunnelHighFlows:
            if flow[3] == '\'A\'':
                tunnelHighAtacks += 1
                tunnelHighAttackTraffic += flow[1]
            else:
                benignHighPassRate += flow[1] * passRate
                benignHighTraffic += flow[1]

        print('======================= DDoS REPORT ======================')
        print('Tunnel Low Attacks: ' + str(tunnelLowAtacks))
        print('Tunnel Low Attacaks Traffic: ' + str(tunnelLowAtackTraffic))
        print('Tunnel High Attacks: ' + str(tunnelHighAtacks))
        print('Tunnel High Attacks Traffic: ' + str(tunnelHighAttackTraffic))
        print('Benign Pass Rate: ' + str((benignLowPassRate + benignHighPassRate)/(benignLowTraffic + benignHighTraffic)))
        print('Filtered Benign Pass Rate: ' + str((filteredBenignLowPassRate + benignHighPassRate)/(benignLowTraffic + benignHighTraffic)))
        print('==========================================================')

    def simulationBySecond(self, trafficFilePath, testMethod):
        seconds = 1
        input = open(trafficFilePath, 'r')
        trafficFile = input.readlines()

        for data in trafficFile:
            if data.startswith('['):
                parsedData = (data[1:len(data) - 2]).replace(' ', '').split(',')
                self.trafficHistoryInsert(int(parsedData[0]), float(parsedData[2]), int(parsedData[1]), parsedData[3], testMethod)
            else:
                if data != '\n':
                    print('Second: ' + str(seconds) + ' Traffic: ' + str(data.replace('\n', '')))
                    seconds += 1
                else:
                    testMethod.tunnelLowFilter()
                    self.generateBasicReport(testMethod)
                    self.generateDDoSReport(testMethod)
                    print('\n')