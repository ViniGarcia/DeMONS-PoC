import bisect
import copy

import Filters

class DeMONS:
#tunnelLowFlows - ordered list of triples (flowPritority, flowIntensity flowID)
#tunnelHighFlows - ordered list of triples (flowPritority, flowIntensity, flowID)
#   flowPriority - float number (0 ~ 1)
#   flowIntensity - integer
#   flowID - string
    tunnelLowFlows = None
    tunnelHighFlows = None

#tunnelLowUse - bandwidth use of low tunnel (integer)
#tunnelHighUse - bandwidth use of high tunnel (integer)
#lastTunnelHighUse - trigger for balance (integer)
    tunnelLowUse = None
    tunnelHighUse = None
    lastTunnelHighUse = None

#tunnelLowUse - bandwidth capacity of low tunnel (integer)
#tunnelHighUse - bandwidth capacity of high tunnel (integer)
    tunnelLowCapacity = None
    tunnelHighCapacity = None

#tunnelHighNormal - normal bandwidth use of high tunnel (float 0 ~ 1)
    tunnelHighNormal = None

#tunnelLowSum - priorities sum form low tunnel (float)
#tunnelHighSum - priorities sum from high tunnel (float)
    tunnelLowSum = None
    tunnelHighSum = None

#tunnelLowDrop - traffic drop by tunnel low filter for each flow (integer)
#tunnelLowDropRate - total traffic dropped vy the filter (integer)
    tunnelLowDrop = None
    tunnelLowDropRate = None

#schedulerData - queue for traffic shapping (not used for policing)
#maxIntervalQueue - how many times the same traffic can be enqueued
    schedulerData = None
    maxIntervalQueue = None

    def __init__(self, lowCapacity, highCapacity, highNormal, schedulerQueue = 0, maxIntervalQueue = 0):
        self.tunnelLowCapacity = lowCapacity
        self.tunnelHighCapacity = highCapacity
        self.tunnelHighNormal = highNormal

        self.tunnelLowFlows = []
        self.tunnelHighFlows = []

        self.tunnelLowUse = 0
        self.tunnelHighUse = 0
        self.lastTunnelHighUse = 0

        self.tunnelLowSum = 0
        self.tunnelHighSum = 0

        self.tunnelLowDrop = {}
        self.tunnelLowDropRate = 0

        self.schedulerData = [schedulerQueue, 0, [], 0]
        self.maxIntervalQueue = maxIntervalQueue


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


    def selectiveFlowAllocation(self, flowID, flowPriority, flowIntensity, flowType, flowQueue = 0):
        if flowQueue == 0:
            flowList = [flowPriority, flowIntensity, flowID, flowType]
        else:
            flowList = [flowPriority, flowIntensity, flowID, flowType, flowQueue]


        if self.tunnelLowUse < self.tunnelHighUse:
            bisect.insort(self.tunnelLowFlows, flowList)
            self.tunnelLowUse += flowIntensity
            self.tunnelLowSum += flowPriority
        else:
            if self.tunnelHighUse/self.tunnelHighCapacity < self.tunnelHighNormal:
                if self.tunnelHighUse + flowIntensity <= self.tunnelHighCapacity:
                    bisect.insort(self.tunnelHighFlows, flowList)
                    self.lastTunnelHighUse = self.tunnelHighUse
                    self.tunnelHighUse += flowIntensity
                    self.tunnelHighSum += flowPriority
                else:
                    bisect.insort(self.tunnelLowFlows, flowList)
                    self.tunnelLowUse += flowIntensity
                    self.tunnelLowSum += flowPriority
            else:
                if self.tunnelHighUse >= self.tunnelHighCapacity:
                    self.condicionalAllocation(flowList)
                else:
                    if self.lastTunnelHighUse/self.tunnelHighCapacity < self.tunnelHighNormal:
                        self.balanceFlows()
                    if flowPriority > self.tunnelHighFlows[0][0]:
                        if self.tunnelHighUse + flowIntensity <= self.tunnelHighCapacity:
                            bisect.insort(self.tunnelHighFlows, flowList)
                            self.lastTunnelHighUse = self.tunnelHighUse
                            self.tunnelHighUse += flowIntensity
                            self.tunnelHighSum += flowPriority
                        else:
                            self.condicionalAllocation(flowList)
                    else:
                        bisect.insort(self.tunnelLowFlows, flowList)
                        self.tunnelLowUse += flowIntensity
                        self.tunnelLowSum += flowPriority


    def tunnelLowFilter(self, mechanism, policy = 0):
        if mechanism == 0:
            Filters.demonsStandard(self, policy)
        elif mechanism == 1:
            Filters.tokenBucketPolicer(self, self.tunnelLowCapacity)
        elif mechanism == 2:
            Filters.leakyBucketShapper(self, self.tunnelLowCapacity)
        else:
            Filters.leakyBucketPriorityShapper(self, self.tunnelLowCapacity, policy)