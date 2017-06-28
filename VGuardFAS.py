import bisect
import copy

class VGuardFAS:
#tunnelLowFlows - ordered list of triples (flowPritority, flowIntensity flowID)
#tunnelHighFlows - ordered list of triples (flowPritority, flowIntensity, flowID)
#   flowPriority - float number (0 ~ 1)
#   flowIntensity - integer
#   flowID - string
    tunnelLowFlows = []
    tunnelHighFlows = []

#tunnelLowUse - bandwidth use of low tunnel (integer)
#tunnelHighUse - bandwidth use of high tunnel (integer)
#lastTunnelHighUse - trigger for balance (integer)
    tunnelLowUse = 0
    tunnelHighUse = 0
    lastTunnelHighUse = 0

#tunnelLowUse - bandwidth capacity of low tunnel (integer)
#tunnelHighUse - bandwidth capacity of high tunnel (integer)
    tunnelLowCapacity = 0
    tunnelHighCapacity = 0

#tunnelHighNormal - normal bandwidth use of high tunnel (float 0 ~ 1)
    tunnelHighNormal = 0

#tunnelLowSum - priorities sum form low tunnel (float)
#tunnelHighSum - priorities sum from high tunnel (float)
    tunnelLowSum = 0
    tunnelHighSum = 0

#tunnelLowDrop - traffic drop by tunnel low filter for each flow (integer)
#tunnelLowDropRate - total traffic dropped vy the filter (integer)
    tunnelLowDrop = {}
    tunnelLowDropRate = 0

    def __init__(self, lowCapacity, highCapacity, highNormal):
        self.tunnelLowCapacity = lowCapacity
        self.tunnelHighCapacity = highCapacity
        self.tunnelHighNormal = highNormal

    def condicionalAllocation(self, flowTriple):
        flowFree = self.tunnelHighCapacity - self.tunnelHighUse
        flowSum = flowFree
        prioritySum = 0
        flowAmount = 0
        for flow in self.tunnelHighFlows:
            if flow[0] < flowTriple[0]:
                flowSum += flow[1]
                prioritySum += flow[0]
                flowAmount += 1
                if flowSum >= flowTriple[1]:
                    for popFlow in list(self.tunnelHighFlows[:flowAmount]):
                        bisect.insort(self.tunnelLowFlows, self.tunnelHighFlows.pop(self.tunnelHighFlows.index(popFlow)))
                    bisect.insort(self.tunnelHighFlows, flowTriple)
                    self.lastTunnelHighUse = self.tunnelHighUse
                    self.tunnelHighUse = self.tunnelHighUse - flowSum + flowFree + flowTriple[1]
                    self.tunnelHighSum = self.tunnelHighSum - prioritySum + flowTriple[0]
                    self.tunnelLowUse += flowSum - flowFree
                    self.tunnelLowSum += prioritySum
                    return True
            else:
                bisect.insort(self.tunnelLowFlows, flowTriple)
                self.tunnelLowUse += flowTriple[1]
                self.tunnelLowSum += flowTriple[0]
                return False

    def balanceFlows(self):
        tunnelLowFlowsCopy = reversed(copy.copy(self.tunnelLowFlows))
        for flow in tunnelLowFlowsCopy:
            if flow[0] > self.tunnelHighFlows[0][0]:
                self.tunnelLowUse -= flow[1]
                self.tunnelLowSum -= flow[0]
                self.condicionalAllocation(self.tunnelLowFlows.pop(self.tunnelLowFlows.index(flow)))
            else:
                break

    def selectiveFlowAllocation(self, flowID, flowPriority, flowIntensity, flowType):
        if self.tunnelLowUse < self.tunnelHighUse:
            bisect.insort(self.tunnelLowFlows,[flowPriority, flowIntensity, flowID, flowType])
            self.tunnelLowUse += flowIntensity
            self.tunnelLowSum += flowPriority
        else:
            if self.tunnelHighUse/self.tunnelHighCapacity < self.tunnelHighNormal:
                if self.tunnelHighUse + flowIntensity <= self.tunnelHighCapacity:
                    bisect.insort(self.tunnelHighFlows,[flowPriority, flowIntensity, flowID, flowType])
                    self.lastTunnelHighUse = self.tunnelHighUse
                    self.tunnelHighUse += flowIntensity
                    self.tunnelHighSum += flowPriority
                else:
                    bisect.insort(self.tunnelLowFlows, [flowPriority, flowIntensity, flowID, flowType])
                    self.tunnelLowUse += flowIntensity
                    self.tunnelLowSum += flowPriority
            else:
                if self.tunnelHighUse >= self.tunnelHighCapacity:
                    self.condicionalAllocation([flowPriority, flowIntensity, flowID, flowType])
                else:
                    if self.lastTunnelHighUse/self.tunnelHighCapacity < self.tunnelHighNormal:
                        self.balanceFlows()
                    if flowPriority > self.tunnelHighFlows[0][0]:
                        if self.tunnelHighUse + flowIntensity <= self.tunnelHighCapacity:
                            bisect.insort(self.tunnelHighFlows, [flowPriority, flowIntensity, flowID, flowType])
                            self.lastTunnelHighUse = self.tunnelHighUse
                            self.tunnelHighUse += flowIntensity
                            self.tunnelHighSum += flowPriority
                        else:
                            self.condicionalAllocation([flowPriority, flowIntensity, flowID, flowType])
                    else:
                        bisect.insort(self.tunnelLowFlows, [flowPriority, flowIntensity, flowID, flowType])
                        self.tunnelLowUse += flowIntensity
                        self.tunnelLowSum += flowPriority

    def tunnelLowFilter(self):
        if self.tunnelLowUse > self.tunnelLowCapacity:
            tunnelDropRate = self.tunnelLowUse - self.tunnelLowCapacity
            self.tunnelLowDrop = {}
            self.tunnelLowDropRate = 0
            for flow in self.tunnelLowFlows:
                flowDrop = flow[1] * ((1-flow[0]) + (flow[0]*0.1))
                if flowDrop < tunnelDropRate:
                    self.tunnelLowDrop[flow[2]] = round(flowDrop, 0)
                    tunnelDropRate -= flowDrop
                    self.tunnelLowDropRate += flowDrop
                else:
                    self.tunnelLowDrop[flow[2]] = round(tunnelDropRate,0)
                    self.tunnelLowDropRate += tunnelDropRate
                    break
        else:
            self.tunnelLowDrop = {}
            self.tunnelLowDropRate = 0