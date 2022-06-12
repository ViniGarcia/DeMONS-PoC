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


#Tokens: Analogia para bytes
#Burst: Tamnho do bucket
#Charge: Quantidade de tokens inicialmente no bucket
#Rate: Taxa de inserção de tokens
#Interval: Tempo em segundos para ativação do rate
def tokenBucketPolicer(testMethod, burst, charge, rate, interval):
	pass


def tokenBucketShapper(testMethod, burst, charge, rate, interval, queue):
	pass


def leakyBucketShapper(testMethod, burst, rate, interval):
	pass