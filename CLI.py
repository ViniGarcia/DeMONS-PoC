import sys
from os import path
from cmd import Cmd

sys.path.insert(0, 'Solutions/')
from VGuard import VGuard
from DeMONS import DeMONS

sys.path.insert(0, 'Simulators/')
from MethodsSimulator import MethodsSimulator
from FlowSimulator import FlowSimulator

class SimulationCLI(Cmd):

	prompt = 'simulator> '
	flows =  FlowSimulator()
	methods = MethodsSimulator()
	
	mechanism = 0
	policy = 0
	report = 1
	output = None

	def do_help(self, args):

		print ('\n############### HELP #################')
		print ('flow -> create a simulation flow summary')
		print ('- arguments for normal flows: N file distribution')
		print ('- arguments for peak flows: P file distribution peak_distribution')
		print ('- arguments for DDoS flows: A file benign_distribution ddos_distribution ddos_start_moment')
		print ('-- file: string')
		print ('-- distributions: N100/30-1, N100/30-2, N500/30, D500/10, P20/40/30, P120/150/30, P200/500/30')
		print ('-- ddos_start_moment: integer')
		print ('')
		print ('vguard -> execute a VGuard solution simulation')
		print ('- arguments: flow_file tunnel_low_cap tunnel_high_cap selective_mode [scheduler_queue_size]')
		print ('-- flow_file: string')
		print ('-- tunnel_low_cap: integer')
		print ('-- tunnel_high_cap: integer')
		print ('-- selective_mode: float (>= 0 and <= 1)')
		print ('-- scheduler_queue_size: integer, optional argument')
		print ('')
		print ('demons -> execute a DeMONS solution simulation')
		print ('- arguments: flow_file tunnel_low_cap tunnel_high_cap selective_mode [scheduler_queue_size]')
		print ('-- flow_file: string')
		print ('-- tunnel_low_cap: integer')
		print ('-- tunnel_high_cap: integer')
		print ('-- selective_mode: float (>= 0 and <= 1)')
		print ('-- scheduler_queue_size: integer, optional argument')
		print ('')
		print ('full -> execute both VGuad and DeMONS simulations')
		print ('- arguments: flow_file tunnel_low_cap tunnel_high_cap selective_mode')
		print ('-- flow_file: string')
		print ('-- tunnel_low_cap: integer')
		print ('-- tunnel_high_cap: integer')
		print ('-- selective_mode: float (>= 0 and <= 1)')
		print ('-- scheduler_queue_size: integer, optional argument')
		print ('')
		print ('reporting -> define how many seconds passes (in the simulation) to create a report')
		print ('- arguments: seconds')
		print ('-- seconds: int (> 0) [standard value is 1]')
		print ('')
		print ('filter -> define which filter to use in the low priority tunnel')
		print ('- arguments: filter_id')
		print ('-- filter_id: int [0: Method Std; 1: Token Bucket Policer; 2: Leaky Bucket Shaper; 3/Std: Leaky Bucket Shaper + Priority Filter]')
		print ('')
		print ('policy -> define which policy to use in filter\'s dropping policy [when required]')
		print ('- arguments: policy_id')
		print ('-- policy_id: int [0: Restrictive; 1: Medium; 2/Std: Permissive]')
		print ('')
		print ('exit -> end simulator')
		print ('######################################\n')


	def do_flow(self, args):

		if len(args) == 0:
			return

		arguments = args.split()

		if len(arguments) < 3:
			print('INVALID ARGUMENTS!')
			return

		if not arguments[0] in ['N', 'P', 'A']:
			print("INVALID TRAFFIC CREATION MODE!")
			return

		if arguments[0] == 'N' and len(arguments) == 3:

			if self.flows.flowCreate(arguments[2], str(arguments[1])):
				print('SUCCESS!!')
				return
			else:
				print('INVALID FLOW ID!!')
				return

		elif arguments[0] == 'A' and len(arguments) == 5:
			
			if int(arguments[4]) < 0:
				print('INVALID ATTACK START TIME!!')
				return

			if self.flows.ddosCreate(arguments[2], arguments[3], int(arguments[4]), str(arguments[1])):
				print('SUCCESS!!')
				return
			else:
				print('INVALID FLOW ID!!')
				return

		elif arguments[0] == 'P' and len(arguments) == 4:

			if self.flows.peakCreate(arguments[2], arguments[3], str(arguments[1])):
				print('SUCCESS!!')
				return
			else:
				print('INVALID FLOW ID!!')
				return

		print('INVALID ARGUMENTS!!')
		return

	def do_vguard(self, args):

		if len(args) == 0:
			return

		arguments = args.split()

		if len(arguments) >= 4:
			
			if int(arguments[1]) < 0:
				print('INVALID TUNNEL LOW CAPACITY!!')
				return

			if int(arguments[2]) < 0:
				print('INVALID TUNNEL HIGH CAPACITY!!')
				return

			if float(arguments[3]) < 0 or float(arguments[3]) > 1:
				print('INVALID SELECTIVE MODE PARAMETER!!')
				return

			if not path.isfile(arguments[0]):
				print('INVALID FILE!!')
				return

			if len(arguments) == 5:
				if int(arguments[4]) < 0:
					print('INVALID SCHEDULER QUEUE CAPACITY!!')
					return
				queue = int(arguments[4])
			elif len(arguments) > 5:
				print('UNRECOGNIZED ARGUMENTS!!')
				return
			else:
				queue = 0
 			
			self.output = open("[F" + str(self.mechanism) + "-P" + str(self.policy) + "]-" + "VGuard-" + arguments[0] + "-" + arguments[1] + "-" + arguments[2] + "-" + arguments[3] + "-" + str(queue) + ".txt", "w+")
			
			if self.output != None:
				self.output.write('=========================== VGUARD TEST START ==========================\n\n')
			print('=========================== VGUARD TEST START ==========================\n')
			self.methods.simulationBySecond(arguments[0], VGuard(int(arguments[1]), int(arguments[2]), float(arguments[3]), queue), self.report, self.mechanism, self.policy, self.output)
			print('============================ VGUARD TEST END ===========================\n')
			if self.output != None:
				self.output.write('============================ VGUARD TEST END ===========================\n\n')
				self.output.close()
			return

		print('MISSING ARGUMENTS!!')
		return

	def do_demons(self, args):

		if len(args) == 0:
			return

		arguments = args.split()

		if len(arguments) >= 4:
			
			if int(arguments[1]) < 0:
				print('INVALID TUNNEL LOW CAPACITY!!')
				return

			if int(arguments[2]) < 0:
				print('INVALID TUNNEL HIGH CAPACITY!!')
				return

			if float(arguments[3]) < 0 or float(arguments[3]) > 1:
				print('INVALID SELECTIVE MODE PARAMETER!!')
				return

			if not path.isfile(arguments[0]):
				print('INVALID FILE!!')
				return

			if len(arguments) == 5:
				if int(arguments[4]) < 0:
					print('INVALID SCHEDULER QUEUE CAPACITY!!')
					return
				queue = int(arguments[4])
			elif len(arguments) > 5:
				print('UNRECOGNIZED ARGUMENTS!!')
				return
			else:
				queue = 0

			self.output = open("[F" + str(self.mechanism) + "-P" + str(self.policy) + "]-" + "DeMONS-" + arguments[0] + "-" + arguments[1] + "-" + arguments[2] + "-" + arguments[3] + "-" + str(queue) + ".txt", "w+")
			
			if self.output != None:
				self.output.write('============================ DEMONS TEST START ==========================\n\n')
			
			print('============================ DEMONS TEST START ==========================\n')
			self.methods.simulationBySecond(arguments[0], DeMONS(int(arguments[1]), int(arguments[2]), float(arguments[3]), queue), self.report, self.mechanism, self.policy, self.output)
			print('============================= DEMONS TEST END ===========================\n')
			if self.output != None:
				self.output.write('============================= DEMONS TEST END ===========================\n\n')
				self.output.close()
			return

		print('MISSING ARGUMENTS!!')
		return

	def do_full(self, args):

		self.do_vguard(args)
		print('\n')
		self.do_demons(args)

	def do_reporting(self, args):

		if len(args) == 0:
			return

		arguments = args.split()

		if len(arguments) != 1:
			print('UNRECOGNIZED ARGUMENTS!!')
			return

		if int(arguments[0]) <= 0:
			print('INVALID REPORTING INTERVAL!!')
			return

		self.report = int(arguments[0])

		print("REPORTING INTERVAL SET TO", self.report, "!!\n")

	def do_filter(self, args):

		availableFilters = {0:"STANDARD", 1:"TOKEN BUCKET POLICER", 2:"LEAKY BUCKET SHAPER", 3:"LEAKY BUCKET SHAPER + POLICER"}

		if len(args) == 0:
			return

		arguments = args.split()

		if len(arguments) != 1:
			print('UNRECOGNIZED ARGUMENTS!!')
			return

		if int(arguments[0]) < 0 or int(arguments[0]) > 3:
			print('INVALID FILTER MECHANISM!!')
			return

		self.mechanism = int(arguments[0])

		print("FILTER MECHANISM SET TO", availableFilters[self.mechanism], "!!\n")

	def do_policy(self, args):

		availablePolicies = {0:"RESTRICTIVE", 1:"MEDIUM", 2:"PERMISSIVE"}

		if len(args) == 0:
			return

		arguments = args.split()

		if len(arguments) != 1:
			print('UNRECOGNIZED ARGUMENTS!!')
			return

		if int(arguments[0]) < 0 or int(arguments[0]) > 2:
			print('INVALID FILTER POLICY!!')
			return

		self.policy = int(arguments[0])

		print("FILTER POLICY SET TO", availablePolicies[self.policy], "!!\n")

	def do_exit(self, args):

		exit()
		

if __name__ == '__main__':

	SimulationCLI().cmdloop()