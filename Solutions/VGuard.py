import math

import Filters

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

#schedulerData - queue for traffic shapping (not used for policing)
    schedulerData = None

    def __init__(self, lowCapacity, highCapacity, highNormal, schedulerQueue = 0):
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

        self.schedulerData = [schedulerQueue, 0, []]

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
        Filters.vguardStandard(self)
        #Filters.tokenBucketPolicer(self, self.tunnelLowCapacity)
        #Filters.leakyBucketShapper(self, self.tunnelLowCapacity)