import math

class VGuard:
#tunnelLowFlows - ordered list of triples (flowPritority, flowIntensity flowID)
#tunnelHighFlows - ordered list of triples (flowPritority, flowIntensity, flowID)
#   flowPriority - float number (0 ~ 1)
#   flowIntensity - integer
#   flowID - string
    tunnelLowFlows = None
    tunnelHighFlows = None

#tunnelLowUse - bandwidth use of low tunnel (integer)
#tunnelHighUse - bandwidth use of high tunnel (integer)
    tunnelLowUse = None
    tunnelHighUse = None

#tunnelLowUse - bandwidth capacity of low tunnel (integer)
#tunnelHighUse - bandwidth capacity of high tunnel (integer)
    tunnelLowCapacity = None
    tunnelHighCapacity = None

#tunnelHighNormal - normal bandwidth use of high tunnel (float 0 ~ 1)
#tunnelHighSum - priorities sum from tunnelHighFlows
#tunnelLowPrioritySum - priorities sum from tunnelLowFlows
    tunnelHighNormal = None
    tunnelHighSum = None
    tunnelLowSum = None

#tunnelLowDrop - traffic drop by tunnel low filter for each flow (integer)
#tunnelLowDropRate - total traffic dropped vy the filter (integer)
    tunnelLowDrop = None
    tunnelLowDropRate = None

    def __init__(self, lowCapacity, highCapacity, highNormal):
        self.tunnelLowCapacity = lowCapacity
        self.tunnelHighCapacity = highCapacity
        self.tunnelHighNormal = highNormal

        self.tunnelLowFlows = []
        self.tunnelHighFlows = []

        self.tunnelLowUse = 0
        self.tunnelHighUse = 0

        self.tunnelLowSum = 0
        self.tunnelHighSum = 0

        self.tunnelLowDrop = {}
        self.tunnelLowDropRate = 0

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
            totalTunnelDrop = self.tunnelLowUse - self.tunnelLowCapacity

            for flow in self.tunnelLowFlows:
                #dropFactor = (1-flow[0]) + (flow[0]*0.1)
                #dropFactor = 1-flow[0]
                dropFactor = ((1 - flow[0]) + (((1 - flow[0]) + (flow[0] * 0.1)) * (tunnelDropRate / totalTunnelDrop)))
                if dropFactor > 1:
                    dropFactor = 1
                flowDrop = flow[1] * dropFactor
                if flowDrop < tunnelDropRate:
                    self.tunnelLowDrop[flow[2]] = round(flowDrop, 0)
                    tunnelDropRate -= flowDrop
                    self.tunnelLowDropRate += flowDrop
                else:
                    self.tunnelLowDrop[flow[2]] = round(tunnelDropRate,0)
                    self.tunnelLowDropRate += tunnelDropRate
                    break