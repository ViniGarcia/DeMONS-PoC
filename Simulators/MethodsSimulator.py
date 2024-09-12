from sys import path
from math import pow
from statistics import mean, stdev

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

        if flowIntensity != 0:
            if isinstance(testMethod, DeMONS):
                testMethod.selectiveFlowAllocation(flowID, flowPriority, flowIntensity, flowType)
            else:
                if isinstance(testMethod, VGuard):
                    testMethod.flowAllocation(flowID, flowPriority, flowIntensity, flowType)


    def removeDeadFlows(self, testMethod):
        for flow in testMethod.tunnelHighFlows:
            if len(flow) == 5:
                testMethod.tunnelHighUse -= flow[1]
                testMethod.tunnelHighSum -= flow[0]
                testMethod.tunnelHighFlows.remove(flow)
        for flow in testMethod.tunnelLowFlows:
            if len(flow) == 5:
                testMethod.tunnelLowUse -= flow[1]
                testMethod.tunnelLowSum -= flow[0]
                testMethod.tunnelLowFlows.remove(flow)


    def queueAllocation(self, testMethod): 
        testMethod.schedulerData[3] = 0

        for flow in testMethod.schedulerData[2]:
            if len(flow) == 4:
                flow.append(1)
            else:
                if flow[4] < testMethod.maxIntervalQueue:
                    flow[4] += 1
                else:
                    testMethod.schedulerData[3] += flow[1]
                    continue

            if isinstance(testMethod, DeMONS):
                testMethod.selectiveFlowAllocation(flow[2], flow[0], flow[1], flow[3], flow[4])
            elif isinstance(testMethod, VGuard):
                testMethod.flowAllocation(flow[2], flow[0], flow[1], flow[3], flow[4])

        testMethod.schedulerData[1] = 0
        testMethod.schedulerData[2] = []  


    def lowTunnelSatisfaction(self, testMethod):
        if testMethod.tunnelLowUse != 0:
            dropRate = 1 - min(1, testMethod.tunnelLowCapacity/testMethod.tunnelLowUse)
        else:
            dropRate = 0
        satisfaction = pow((1 - dropRate),2)
        maxSatisfaction = 0
        currentSatisfaction = 0

        for flow in testMethod.tunnelLowFlows:
            currentSatisfaction += flow[1] * flow[0] * satisfaction
            maxSatisfaction += flow[1] * flow[0]

        return [currentSatisfaction, maxSatisfaction]


    def lowFilteredTunnelSatisfaction(self, testMethod):
        if testMethod.tunnelLowUse != 0:
            dropRate = 1 - min(1, testMethod.tunnelLowCapacity/(testMethod.tunnelLowUse - testMethod.tunnelLowDropRate))
        else:
            dropRate = 0
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
        if testMethod.tunnelHighUse != 0:
            dropRate = 1 - min(1, testMethod.tunnelHighCapacity/testMethod.tunnelHighUse)
        else:
            dropRate = 0
        satisfaction = pow((1 - dropRate),2)
        maxSatisfaction = 0
        currentSatisfaction = 0

        for flow in testMethod.tunnelHighFlows:
            currentSatisfaction += flow[1] * flow[0] * satisfaction
            maxSatisfaction += flow[1] * flow[0]

        return [currentSatisfaction, maxSatisfaction]


    def generateBasicReport(self, testMethod, outputFile = None):
        lowSatisfaction = self.lowTunnelSatisfaction(testMethod)
        lowFilteredSatisfaction = self.lowFilteredTunnelSatisfaction(testMethod)
        highSatisfaction = self.highTunnelSatisfaction(testMethod)

        if outputFile == None:
            print('====================== BASIC REPORT ======================')
            print('Low Tunnel Flows Amount: ' + str(len(testMethod.tunnelLowFlows)))
            print('Low Tunnel Flows Priority Sum: ' + str(abs(round(testMethod.tunnelLowSum, 4))))
            print('Low Tunnel Crossing Traffic: ' + str(testMethod.tunnelLowUse))
            print('Low Tunnel Current Satisfaction: ' + str(lowSatisfaction[0]))
            print('Low Tunnel Filtered Satisfaction: ' + str(lowFilteredSatisfaction[0]))
            print('Low Tunnel Filtered Maximum Satisfaction: ' + str(lowFilteredSatisfaction[1]))
            print('Low Tunnel Maximum Satisfaction: ' + str(lowSatisfaction[1]))
            print('High Tunnel Flows Amount: ' + str(len(testMethod.tunnelHighFlows)))
            print('High Tunnel Flows Priority Sum: ' + str(abs(round(testMethod.tunnelHighSum, 4))))
            print('High Tunnel Crossing Traffic: ' + str(testMethod.tunnelHighUse))
            print('High Tunnel Current Satisfaction: ' + str(highSatisfaction[0]))
            print('High Tunnel Maximum Satisfaction: ' + str(highSatisfaction[1]))
            print('==========================================================')
        else:
            outputFile.write('====================== BASIC REPORT ======================\n')
            outputFile.write('Low Tunnel Flows Amount: ' + str(len(testMethod.tunnelLowFlows)) + "\n")
            outputFile.write('Low Tunnel Flows Priority Sum: ' + str(abs(round(testMethod.tunnelLowSum, 4))) + "\n")
            outputFile.write('Low Tunnel Crossing Traffic: ' + str(testMethod.tunnelLowUse) + "\n")
            outputFile.write('Low Tunnel Current Satisfaction: ' + str(lowSatisfaction[0]) + "\n")
            outputFile.write('Low Tunnel Filtered Satisfaction: ' + str(lowFilteredSatisfaction[0]) + "\n")
            outputFile.write('Low Tunnel Filtered Maximum Satisfaction: ' + str(lowFilteredSatisfaction[1]) + "\n")
            outputFile.write('Low Tunnel Maximum Satisfaction: ' + str(lowSatisfaction[1]) + "\n")
            outputFile.write('High Tunnel Flows Amount: ' + str(len(testMethod.tunnelHighFlows)) + "\n")
            outputFile.write('High Tunnel Flows Priority Sum: ' + str(abs(round(testMethod.tunnelHighSum, 4))) + "\n")
            outputFile.write('High Tunnel Crossing Traffic: ' + str(testMethod.tunnelHighUse) + "\n")
            outputFile.write('High Tunnel Current Satisfaction: ' + str(highSatisfaction[0]) + "\n")
            outputFile.write('High Tunnel Maximum Satisfaction: ' + str(highSatisfaction[1]) + "\n")
            outputFile.write('==========================================================\n')


    def generateFilterReport(self, testMethod, outputFile = None):
        priorities = [0]*10
        traffic = [0]*10

        for flow in testMethod.tunnelLowFlows:
            priorities[int(flow[0]*10)-1] += 1
            traffic[int(flow[0]*10)-1] += flow[1]

        if outputFile == None:
            print('====================== FILTER REPORT ======================')
            for index in range(0,10):
                print('Priority: ' + str(index+1) + ' Flow Amount: ' + str(priorities[index]) + ' Traffic: ' + str(traffic[index]))
            print('Filter Drop Rate: ' + str(testMethod.tunnelLowDropRate))
            print('After Filter Traffic: ' + str(testMethod.tunnelLowUse - testMethod.tunnelLowDropRate))
            print('After Filter Tunnel Drop Rate: ' + str((testMethod.tunnelLowUse - testMethod.tunnelLowDropRate)/len(testMethod.tunnelLowFlows)))
            print('==========================================================')
        else:
            outputFile.write('====================== FILTER REPORT ======================\n')
            for index in range(0,10):
                outputFile.write('Priority: ' + str(index+1) + ' Flow Amount: ' + str(priorities[index]) + ' Traffic: ' + str(traffic[index]) + "\n")
            outputFile.write('Filter Drop Rate: ' + str(testMethod.tunnelLowDropRate) + "\n")
            outputFile.write('After Filter Traffic: ' + str(testMethod.tunnelLowUse - testMethod.tunnelLowDropRate) + "\n")
            outputFile.write('After Filter Tunnel Drop Rate: ' + str((testMethod.tunnelLowUse - testMethod.tunnelLowDropRate)/len(testMethod.tunnelLowFlows)) + "\n")
            outputFile.write('==========================================================\n')


    def generateQueueReport(self, testMethod, outputFile = None):
        priorities = []
        traffic = []
        if testMethod.schedulerData[1] <= 0:
            priorities += [0.0,0.0]
            traffic += [0,0]
        else:
            for flow in testMethod.schedulerData[2]:
                traffic.append(flow[1])
                priorities.append(flow[0])

        if outputFile == None:
            print('====================== QUEUE REPORT =======================')
            print('Queued Traffic Total: ' + str(sum(traffic)))
            print('Queued Flows Priority Total: ' + str(round(sum(priorities), 2)))
            print('Queued Flows Priority Mean: ' + str(round(mean(priorities), 2)))
            print('Queued Flows Priority Stdev: ' + str(round(stdev(priorities), 2)))
            print('==========================================================')
        else:
            outputFile.write('====================== QUEUE REPORT =======================\n')
            outputFile.write('Queued Traffic Total: ' + str(sum(traffic)) + "\n")
            outputFile.write('Queued Flows Priority Total: ' + str(round(sum(priorities), 2)) + "\n")
            outputFile.write('Queued Flows Priority Mean: ' + str(round(mean(priorities), 2)) + "\n")
            outputFile.write('Queued Flows Priority Stdev: ' + str(round(stdev(priorities), 2)) + "\n")
            outputFile.write('==========================================================\n')


    def generateDDoSReport(self, testMethod, outputFile = None):
        benignLowPassRate = 0
        benignHighPassRate = 0
        filteredBenignLowPassRate = 0
        benignLowTraffic = 0
        benignHighTraffic = 0
        tunnelLowAtacks = 0
        tunnelLowAtackTraffic = 0
        tunnelHighAtacks = 0
        tunnelHighAttackTraffic = 0

        if testMethod.tunnelLowUse != 0:
            passRate = min(1, testMethod.tunnelLowCapacity / testMethod.tunnelLowUse)
        else:
            passRate = 1

        if testMethod.tunnelLowUse != 0:
            filteredPassRate = min(1, testMethod.tunnelLowCapacity / (testMethod.tunnelLowUse - testMethod.tunnelLowDropRate))
        else:
            filteredPassRate = 1

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

        if testMethod.tunnelHighUse != 0:
            passRate = min(1, testMethod.tunnelHighCapacity / testMethod.tunnelHighUse)
        else:
            passRate = 1
        for flow in testMethod.tunnelHighFlows:
            if flow[3] == '\'A\'':
                tunnelHighAtacks += 1
                tunnelHighAttackTraffic += flow[1]
            else:
                benignHighPassRate += flow[1] * passRate
                benignHighTraffic += flow[1]

        if outputFile == None:
            print('======================= DDoS REPORT ======================')
            print('Tunnel Low Attacks: ' + str(tunnelLowAtacks))
            print('Tunnel Low Attacaks Traffic: ' + str(tunnelLowAtackTraffic))
            print('Tunnel High Attacks: ' + str(tunnelHighAtacks))
            print('Tunnel High Attacks Traffic: ' + str(tunnelHighAttackTraffic))
            if benignLowTraffic != 0 or benignHighTraffic != 0:
                print('Benign Pass Rate: ' + str((benignLowPassRate + benignHighPassRate)/(benignLowTraffic + benignHighTraffic)))
                print('Filtered Benign Pass Rate: ' + str((filteredBenignLowPassRate + benignHighPassRate)/(benignLowTraffic + benignHighTraffic)))
            else:
                print('Benign Pass Rate: 0')
                print('Filtered Benign Pass Rate: 0')
            print('==========================================================')
        else:
            outputFile.write('======================= DDoS REPORT ======================\n')
            outputFile.write('Tunnel Low Attacks: ' + str(tunnelLowAtacks) + "\n")
            outputFile.write('Tunnel Low Attacaks Traffic: ' + str(tunnelLowAtackTraffic) + "\n")
            outputFile.write('Tunnel High Attacks: ' + str(tunnelHighAtacks) + "\n")
            outputFile.write('Tunnel High Attacks Traffic: ' + str(tunnelHighAttackTraffic) + "\n")
            if benignLowTraffic != 0 or benignHighTraffic != 0:
                outputFile.write('Benign Pass Rate: ' + str((benignLowPassRate + benignHighPassRate)/(benignLowTraffic + benignHighTraffic)) + "\n")
                outputFile.write('Filtered Benign Pass Rate: ' + str((filteredBenignLowPassRate + benignHighPassRate)/(benignLowTraffic + benignHighTraffic)) + "\n")
            else:
                outputFile.write('Benign Pass Rate: 0\n')
                outputFile.write('Filtered Benign Pass Rate: 0\n')
            outputFile.write('==========================================================\n')


    #METHOD: simulationBySecond
    # The main method to execute the simulations -- creates a schedule for executing the simulator routines.
    # It is relevant to note that this method assumes that the "testMethod" class has standard methods (template).
    # trafficFilePath: a file containing per-second flows data
    # testMethod: DeMONS or VGuard classes (at the moment) -- it is easy to expand the number of methods (new classes with standard methods)
    # reportInterval: calculate evaluation metrics at X seconds of the simulation (1 -> second by second; 2 -> 2 by 2 seconds; ...)
    # filterMechanism: filter mechanism ID for the low priority tunnel [0: Method Std; 1: Token Bucket Policer; 2: Leaky Bucket Shaper; 3..: Leaky Bucket Shaper + Priority Filter]
    # filterPolicy: filter policy ID (sometimes not required) [0: Restrictive; 1: Medium; 2: Permissive]
    #TODO: A FILA NÃO ESTÁ SENDO 100% APROVEITADA EM CENÁRIOS DE SOBRECARGA -- VERIFICAR O QUE PODE ESTAR GERANDO ESSE FENOMENO
    #TODO: OS CANAIS NÃO ESTÃO SENDO 100% APROVEITADOS -- VERIFICAR O QUE PODE ESTAR CAUSANDO ESSE FENOMENO
    def simulationBySecond(self, trafficFilePath, testMethod, reportInterval = 1, filterMechanism = 0, filterPolicy = 0, outputFile = None):
        seconds = 1
        inputData = open(trafficFilePath, 'r')
        trafficFile = inputData.readlines()
        inputData.close()

        for data in trafficFile:
            if data.startswith('['):
                parsedData = (data[1:len(data) - 2]).replace(' ', '').split(',')
                #parsedData -> [0](ID), [2](reputation), [1](traffic), [3](class)
                self.trafficHistoryInsert(int(parsedData[0]), float(parsedData[2]), int(parsedData[1]), parsedData[3], testMethod)
            else:
                if data != '\r\n' and data != '\n':
                    
                    #Removing residual flows regarding transmissions from queues (if no queue is used, the function does not execute any operation)
                    self.removeDeadFlows(testMethod)
                    
                    print('Second: ' + str(seconds) + ' Traffic: ' + str(data.replace('\n', '') + ' Queued: ' + str(testMethod.schedulerData[1])))
                    if outputFile != None:
                        outputFile.write('\nSecond: ' + str(seconds) + ' Traffic: ' + str(data.replace('\n', '')) + "\n")
                    seconds += 1
                else:

                    #Inserting flows from the queue into the low-priority tunnel to compete for resources
                    self.queueAllocation(testMethod)

                    nonQueuedData = len(testMethod.tunnelLowFlows)
                    testMethod.tunnelLowFilter(filterMechanism, filterPolicy)
                    
                    if ((seconds-2) % reportInterval) == 0:
                        self.generateBasicReport(testMethod, outputFile)
                        self.generateDDoSReport(testMethod, outputFile)
                        self.generateQueueReport(testMethod, outputFile)
                    print('\n')

                    # Updating the flows crossing the low priority tunnel by removing the unqueued traffic and recalculating bandwidth usage and priority sum attributes;
                    # sometimes we do not use shapers to queue flows, but I am not considering it.
                    testMethod.tunnelLowFlows = testMethod.tunnelLowFlows[:nonQueuedData]
                    testMethod.tunnelLowUse = 0
                    testMethod.tunnelLowSum = 0
                    for flow in testMethod.tunnelLowFlows:
                        testMethod.tunnelLowUse += flow[1]
                        testMethod.tunnelLowSum += flow[0]