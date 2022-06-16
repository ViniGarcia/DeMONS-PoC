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
	report = 1

	def do_help(self, args):

		print ('\n############### HELP #################')
		print ('flow -> create a simulation flow summary')
		print ('- arguments for normal flows: file distribution')
		print ('- arguments for DDoS flows: file benign_distribution ddos_distribution ddos_start_moment')
		print ('-- file: string')
		print ('-- distributions: N100/30-1, N100/30-2, N500/30, D500/10')
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
		print ('exit -> end simulator')
		print ('######################################\n')


	def do_flow(self, args):

		global getFunction_100_0_30_F1
		global getFunction_100_0_30_F2
		global getFunction_500_0_30
		global getFunctionDDoS_500_10

		if len(args) == 0:
			return

		arguments = args.split()

		if len(arguments) == 2:

			if self.flows.flowCreate(arguments[1], str(arguments[0])):
				print('SUCCESS!!')
				return
			else:
				print('INVALID FLOW ID!!')
				return

		if len(arguments) == 4:
			
			if int(arguments[3]) < 0:
				print('INVALID ATTACK START TIME!!')
				return

			if self.flows.ddosCreate(arguments[1], arguments[2], int(arguments[3]), str(arguments[0])):
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
 
			print('=========================== VGUARD TEST START ==========================\n')
			self.methods.simulationBySecond(arguments[0], VGuard(int(arguments[1]), int(arguments[2]), float(arguments[3]), queue), self.report)
			print('============================ VGUARD TEST END ===========================\n')
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

			print('============================ DEMONS TEST START ==========================\n')
			self.methods.simulationBySecond(arguments[0], DeMONS(int(arguments[1]), int(arguments[2]), float(arguments[3]), queue), self.report)
			print('============================= DEMONS TEST END ===========================\n')
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

	def do_exit(self, args):

		exit()
		

if __name__ == '__main__':

	SimulationCLI().cmdloop()