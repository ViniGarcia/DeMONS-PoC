import copy
import math

def demonsStandard(testMethod):
	if testMethod.tunnelLowUse > testMethod.tunnelLowCapacity:
		tunnelDropRate = testMethod.tunnelLowUse - testMethod.tunnelLowCapacity
		totalTunnelDrop = testMethod.tunnelLowUse - testMethod.tunnelLowCapacity
		testMethod.tunnelLowDrop = {}
		testMethod.tunnelLowDropRate = 0
		for flow in testMethod.tunnelLowFlows:
			#dropFactor = (1-flow[0]) + (flow[0]*0.1)
			#dropFactor = 1-flow[0]
			dropFactor = ((1 - flow[0]) + (((1 - flow[0]) + (flow[0] * 0.1)) * (tunnelDropRate / totalTunnelDrop)))
			if dropFactor > 1:
				dropFactor = 1
			flowDrop = flow[1] * dropFactor
			if flowDrop < tunnelDropRate:
				testMethod.tunnelLowDrop[flow[2]] = round(flowDrop, 0)
				tunnelDropRate -= flowDrop
				testMethod.tunnelLowDropRate += flowDrop
			else:
				testMethod.tunnelLowDrop[flow[2]] = round(tunnelDropRate,0)
				testMethod.tunnelLowDropRate += tunnelDropRate
				break
	else:
		testMethod.tunnelLowDrop = {}
		testMethod.tunnelLowDropRate = 0


def vguardStandard(testMethod):
	testMethod.tunnelLowDrop = {}
	testMethod.tunnelLowDropRate = 0

	if testMethod.tunnelLowUse > testMethod.tunnelLowCapacity:
		tunnelDropRate = testMethod.tunnelLowUse - testMethod.tunnelLowCapacity
		totalTunnelDrop = testMethod.tunnelLowUse - testMethod.tunnelLowCapacity

		for flow in testMethod.tunnelLowFlows:
			#dropFactor = (1-flow[0]) + (flow[0]*0.1)
			#dropFactor = 1-flow[0]
			dropFactor = ((1 - flow[0]) + (((1 - flow[0]) + (flow[0] * 0.1)) * (tunnelDropRate / totalTunnelDrop)))
			if dropFactor > 1:
				dropFactor = 1
			flowDrop = flow[1] * dropFactor
			if flowDrop < tunnelDropRate:
				testMethod.tunnelLowDrop[flow[2]] = round(flowDrop, 0)
				tunnelDropRate -= flowDrop
				testMethod.tunnelLowDropRate += flowDrop
			else:
				testMethod.tunnelLowDrop[flow[2]] = round(tunnelDropRate,0)
				testMethod.tunnelLowDropRate += tunnelDropRate
				break


def tokenBucketPolicer(testMethod, burst):
	testMethod.tunnelLowDrop = {}
	testMethod.tunnelLowDropRate = 0

	if testMethod.tunnelLowUse > burst:
		dropFactor = (testMethod.tunnelLowUse - burst) / testMethod.tunnelLowUse

		for flow in testMethod.tunnelLowFlows:
			flowDrop = flow[1] * dropFactor
			testMethod.tunnelLowDrop[flow[2]] = round(flowDrop, 0)
			testMethod.tunnelLowDropRate += flowDrop
		

def leakyBucketShapper(testMethod, rate):
	testMethod.tunnelLowDrop = {}
	testMethod.tunnelLowDropRate = 0

	queueFree = testMethod.schedulerData[0] - testMethod.schedulerData[1]

	if testMethod.tunnelLowUse > rate:
		tunnelDropRate = testMethod.tunnelLowUse - rate
		dropFactor = tunnelDropRate / testMethod.tunnelLowUse
		
		queueFactor = queueFree / tunnelDropRate
		if queueFactor > 1:
			queueFactor = 1

		for flow in testMethod.tunnelLowFlows:
			flowDrop = math.floor(flow[1] * dropFactor)
			
			if queueFactor > 0:
				queueData = copy.deepcopy(flow)
				queueData[1] = math.floor(flowDrop * queueFactor)
				testMethod.schedulerData[2].append(queueData)
				testMethod.schedulerData[1] += queueData[1]
				flowDrop -= queueData[1]

			if flowDrop > 0:
				testMethod.tunnelLowDrop[flow[2]] = flowDrop
				testMethod.tunnelLowDropRate += flowDrop
	else:
		if testMethod.schedulerData[1] != 0:
			remainingBandwidth = rate - testMethod.tunnelLowUse
			passingFactor = remainingBandwidth/testMethod.schedulerData[1]
			if passingFactor >= 1:
				testMethod.tunnelLowUse += testMethod.schedulerData[1]
				testMethod.schedulerData[1] = 0
				testMethod.tunnelLowFlows += testMethod.schedulerData[2]
				for flow in testMethod.schedulerData[2]:
					testMethod.tunnelLowSum += flow[0]
				testMethod.schedulerData[2] = []
			else:
				for flow in testMethod.schedulerData[2]:
					releasedData = math.floor(flow[1] * passingFactor)
					testMethod.tunnelLowUse += releasedData
					testMethod.schedulerData[1] -= releasedData
					flow[1] -= releasedData

					releasedFlow = copy.deepcopy(flow)
					releasedFlow[1] = releasedData
					testMethod.tunnelLowFlows.append(releasedFlow)
					testMethod.tunnelLowSum += releasedFlow[0]


def leakyBucketPriorityShapper(testMethod, rate):
	testMethod.tunnelLowDrop = {}
	testMethod.tunnelLowDropRate = 0

	queueFree = testMethod.schedulerData[0] - testMethod.schedulerData[1]

	if testMethod.tunnelLowUse > rate:
		tunnelDropRate = testMethod.tunnelLowUse - rate
		totalTunnelDrop = testMethod.tunnelLowUse - rate

		for flow in testMethod.tunnelLowFlows:
		
			if tunnelDropRate <= 0:
				break

			#dropFactor = ((1 - flow[0]) + (((1 - flow[0]) + (flow[0] * 0.1)) * (tunnelDropRate / totalTunnelDrop)))
			#dropFactor = (1-flow[0]) + (flow[0]*0.1)
			dropFactor = 1-flow[0]
			if dropFactor > 1:
				dropFactor = 1
			queueFactor = (1 - dropFactor)
			flowDrop = math.floor(flow[1] * dropFactor)

			if queueFree > 0:
				flowQueue = math.floor(flow[1] * queueFactor)
				if queueFree < flowQueue:
					flowQueue = queueFree
			else:
				flowQueue = 0

			if flowQueue > 0:
				queueData = copy.deepcopy(flow)
				queueData[1] = flowQueue
				testMethod.schedulerData[2].append(queueData)
				testMethod.schedulerData[1] += queueData[1]

				flowDrop -= queueData[1]
				queueFree -= queueData[1]
				tunnelDropRate -= queueData[1]

			if flowDrop > 0:
				testMethod.tunnelLowDrop[flow[2]] = flowDrop
				testMethod.tunnelLowDropRate += flowDrop
				tunnelDropRate -= flowDrop
	else:
		if testMethod.schedulerData[1] != 0:
			remainingBandwidth = rate - testMethod.tunnelLowUse
			passingFactor = remainingBandwidth/testMethod.schedulerData[1]
			if passingFactor >= 1:
				testMethod.tunnelLowUse += testMethod.schedulerData[1]
				testMethod.schedulerData[1] = 0
				testMethod.tunnelLowFlows += testMethod.schedulerData[2]
				for flow in testMethod.schedulerData[2]:
					testMethod.tunnelLowSum += flow[0]
				testMethod.schedulerData[2] = []
			else:
				for flow in testMethod.schedulerData[2]:
					releasedData = math.floor(flow[1] * passingFactor)
					testMethod.tunnelLowUse += releasedData
					testMethod.schedulerData[1] -= releasedData
					flow[1] -= releasedData

					releasedFlow = copy.deepcopy(flow)
					releasedFlow[1] = releasedData
					testMethod.tunnelLowFlows.append(releasedFlow)
					testMethod.tunnelLowSum += releasedFlow[0]