import copy
import math

# FUNCTION: demonsStandard
# Standard DeMONS policer from the first article
# All the operations modify the attributes of the DeMONS or VGuard class
def demonsStandard(testMethod, policy):
	if testMethod.tunnelLowUse > testMethod.tunnelLowCapacity:
		tunnelDropRate = testMethod.tunnelLowUse - testMethod.tunnelLowCapacity
		totalTunnelDrop = testMethod.tunnelLowUse - testMethod.tunnelLowCapacity
		testMethod.tunnelLowDrop = {}
		testMethod.tunnelLowDropRate = 0
		for flow in testMethod.tunnelLowFlows:
			if policy == 0:
				dropFactor = ((1 - flow[0]) + (((1 - flow[0]) + (flow[0] * 0.1)) * (tunnelDropRate / totalTunnelDrop)))
			elif policy == 1:
				dropFactor = (1-flow[0]) + (flow[0]*0.1)
			else:
				dropFactor = 1-flow[0]
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


# FUNCTION: vguardStandard
# Standard VGuard policer from the DeMONS article
# All the operations modify the attributes of the DeMONS or VGuard class
def vguardStandard(testMethod, policy):
	testMethod.tunnelLowDrop = {}
	testMethod.tunnelLowDropRate = 0

	if testMethod.tunnelLowUse > testMethod.tunnelLowCapacity:
		tunnelDropRate = testMethod.tunnelLowUse - testMethod.tunnelLowCapacity
		totalTunnelDrop = testMethod.tunnelLowUse - testMethod.tunnelLowCapacity

		for flow in testMethod.tunnelLowFlows:
			if policy == 0:
				dropFactor = ((1 - flow[0]) + (((1 - flow[0]) + (flow[0] * 0.1)) * (tunnelDropRate / totalTunnelDrop)))
			elif policy == 1:
				dropFactor = (1-flow[0]) + (flow[0]*0.1)
			else:
				dropFactor = 1-flow[0]
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

# FUNCTION: tokenBucketPolicer
# Classic token bucket policer -- it do not work so well in the simulator
def tokenBucketPolicer(testMethod, burst):
	testMethod.tunnelLowDrop = {}
	testMethod.tunnelLowDropRate = 0

	if testMethod.tunnelLowUse > burst:
		dropFactor = (testMethod.tunnelLowUse - burst) / testMethod.tunnelLowUse

		for flow in testMethod.tunnelLowFlows:

			if flow[1] == 0:
				continue

			flowDrop = flow[1] * dropFactor
			testMethod.tunnelLowDrop[flow[2]] = round(flowDrop, 0)
			testMethod.tunnelLowDropRate += flowDrop
		

# FUNCTION: leakyBucketShapper
# Classic leaky bucket shaper -- it uses the schedulerData attribute of the VGuard and DeMONS classes.
# The shaper is working well, but it required some modifications at the MethodsSimulator lass, specifically
# in the simulationBySecond method
def leakyBucketShapper(testMethod, rate):
	testMethod.tunnelLowDrop = {}
	testMethod.tunnelLowDropRate = 0

	queueFree = testMethod.schedulerData[0] - testMethod.schedulerData[1]

	#Se o uso do túnel de baixa prioridade superou o limite suportado com os novos fluxos
	if testMethod.tunnelLowUse > rate:
		#Quantidade de tráfego que precisa ser descartado
		tunnelDropRate = testMethod.tunnelLowUse - rate
		#Porcentagem de tráfego que precisa ser descartado
		dropFactor = tunnelDropRate / testMethod.tunnelLowUse
		
		#Fator de armazenamento do tráfego na fila baseado no que está liberado
		queueFactor = queueFree / tunnelDropRate
		if queueFactor > 1:
			queueFactor = 1

		removeFlows = []
		for flow in testMethod.tunnelLowFlows:

			flowDrop = math.floor(flow[1] * dropFactor)
			
			#Se existe necessidade de enfileiramento (queueFactor > 0), então o fluxo é efileirado segundo o fator necessário
			if queueFactor > 0:
				queueData = copy.deepcopy(flow)
				queueData[1] = math.ceil(flowDrop * queueFactor)
				if queueData[1] != 0 and queueFree >= queueData[1]:
					testMethod.schedulerData[2].append(queueData)
					testMethod.schedulerData[1] += queueData[1]
					flowDrop -= queueData[1]
					queueFree -= queueData[1]

					flow[1] -= queueData[1]
					testMethod.tunnelLowUse -= queueData[1]
					#Se todos os pacotes do fluxo foram enfileirados, ele será removido da análise de passagem à posteriori
					if flow[1] == 0:
						removeFlows.append(flow)

			#Após o enfileiramento, se ainda restar tráfego que não pode ser tratado, deve ser informado o seu descarte
			if flowDrop > 0:
				testMethod.tunnelLowDrop[flow[2]] = flowDrop
				testMethod.tunnelLowDropRate += flowDrop

		#Para os fluxos completamente enfileirados, remova-os dos candidatos à passarem pelo canal de baixa prioridade
		for flow in removeFlows:
			testMethod.tunnelLowFlows.remove(flow)
			testMethod.tunnelLowSum -= flow[0]
	#Se o uso do tunel de baixa prioridade não superou o limite suportado com os novos fluxos
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
					if releasedData > 0:
						testMethod.tunnelLowUse += releasedData
						testMethod.schedulerData[1] -= releasedData
						flow[1] -= releasedData

						releasedFlow = copy.deepcopy(flow)
						releasedFlow[1] = releasedData
						testMethod.tunnelLowFlows.append(releasedFlow)
						testMethod.tunnelLowSum += releasedFlow[0]


# FUNCTION: leakyBucketPriorityShapper
# Classic leaky bucket shaper plus a priority-based filter for executing dropping routines (when required)
# -- it uses the schedulerData attribute of the VGuard and DeMONS classes.
# The shaper is working well, but it required some modifications at the MethodsSimulator lass, specifically
# in the simulationBySecond method
def leakyBucketPriorityShapper(testMethod, rate, policy):
	testMethod.tunnelLowDrop = {}
	testMethod.tunnelLowDropRate = 0

	queueFree = testMethod.schedulerData[0] - testMethod.schedulerData[1]

	if testMethod.tunnelLowUse > rate:
		tunnelDropRate = testMethod.tunnelLowUse - rate
		totalTunnelDrop = testMethod.tunnelLowUse - rate

		removeFlows = []
		for flow in testMethod.tunnelLowFlows:
		
			if tunnelDropRate <= 0:
				break

			if tunnelDropRate <= queueFree:			#This strategy allows the queue to be fully utilized when there is enough memory to handle all incoming traffic (this may be controversial, as policers will not take effect in such cases)
				dropFactor = 0						#Enqueuing all traffic may not be a good idea during an attack.
			elif policy == 0:
				dropFactor = ((1 - flow[0]) + (((1 - flow[0]) + (flow[0] * 0.1)) * (tunnelDropRate / totalTunnelDrop)))
			elif policy == 1:
				dropFactor = (1-flow[0]) + (flow[0]*0.1)
			else:
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

				flow[1] -= queueData[1]	
				testMethod.tunnelLowUse -= queueData[1]
				if flow[1] == 0:
					removeFlows.append(flow)

			if flowDrop > 0:
				testMethod.tunnelLowDrop[flow[2]] = flowDrop
				testMethod.tunnelLowDropRate += flowDrop
				tunnelDropRate -= flowDrop

		for flow in removeFlows:
			testMethod.tunnelLowFlows.remove(flow)
			testMethod.tunnelLowSum -= flow[0]
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
					if releasedData > 0:
						testMethod.tunnelLowUse += releasedData
						testMethod.schedulerData[1] -= releasedData
						flow[1] -= releasedData

						releasedFlow = copy.deepcopy(flow)
						releasedFlow[1] = releasedData
						testMethod.tunnelLowFlows.append(releasedFlow)
						testMethod.tunnelLowSum += releasedFlow[0]