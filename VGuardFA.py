import math

class VGuardFA:
#tunnelLowFlows - ordered list of triples (flowPritority, flowIntensity flowID)
#tunnelHighFlows - ordered list of triples (flowPritority, flowIntensity, flowID)
#   flowPriority - float number (0 ~ 1)
#   flowIntensity - integer
#   flowID - string
    tunnelLowFlows = []
    tunnelHighFlows = []

#tunnelLowUse - bandwidth use of low tunnel (integer)
#tunnelHighUse - bandwidth use of high tunnel (integer)
    tunnelLowUse = 0
    tunnelHighUse = 0

#tunnelLowUse - bandwidth capacity of low tunnel (integer)
#tunnelHighUse - bandwidth capacity of high tunnel (integer)
    tunnelLowCapacity = 0
    tunnelHighCapacity = 0

#tunnelHighNormal - normal bandwidth use of high tunnel (float 0 ~ 1)
#tunnelHighSum - priorities sum from tunnelHighFlows
#tunnelLowPrioritySum - priorities sum from tunnelLowFlows
    tunnelHighNormal = 0
    tunnelHighSum = 0
    tunnelLowSum = 0

#tunnelLowDrop - traffic drop by tunnel low filter for each flow (integer)
#tunnelLowDropRate - total traffic dropped vy the filter (integer)
    tunnelLowDrop = {}
    tunnelLowDropRate = 0

    def __init__(self, lowCapacity, highCapacity, highNormal):
        self.tunnelLowCapacity = lowCapacity
        self.tunnelHighCapacity = highCapacity
        self.tunnelHighNormal = highNormal

    def flowAllocation(self, flowID, flowPriority, flowIntensity, flowType):
        if self.tunnelLowUse < self.tunnelHighUse:
            self.tunnelLowFlows.append([flowPriority, flowIntensity, flowID, flowType])
            self.tunnelLowUse += flowIntensity
            self.tunnelLowSum += flowPriority
        else:
            if self.tunnelHighUse/self.tunnelHighCapacity < self.tunnelHighNormal:
                self.tunnelHighFlows.append([flowPriority, flowIntensity, flowID, flowType])
                self.tunnelHighUse += flowIntensity
                self.tunnelHighSum += flowPriority
            else:
                if self.tunnelHighUse > self.tunnelHighCapacity:
                    self.tunnelLowFlows.append([flowPriority, flowIntensity, flowID, flowType])
                    self.tunnelLowUse += flowIntensity
                    self.tunnelLowSum += flowPriority
                else:
                    if flowPriority > self.tunnelHighSum/len(self.tunnelHighFlows):
                        self.tunnelHighFlows.append([flowPriority, flowIntensity, flowID, flowType])
                        self.tunnelHighUse += flowIntensity
                        self.tunnelHighSum += flowPriority
                    else:
                        self.tunnelLowFlows.append([flowPriority, flowIntensity, flowID, flowType])
                        self.tunnelLowUse += flowIntensity
                        self.tunnelLowSum += flowPriority

    def tunnelLowFilter(self):
        self.tunnelLowDrop = {}
        self.tunnelLowDropRate = 0

        if self.tunnelLowUse > self.tunnelLowCapacity:
            tunnelDropRate = self.tunnelLowUse - self.tunnelLowCapacity

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