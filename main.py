import sys
from os import path
from VGuardFA import VGuardFA
from VGuardFAS import VGuardFAS
from MethodsSimulator import MethodsSimulator

def help():
    print('=========================== HELP =========================')
    print('USAGE: python main.py TLC THC SM IFP TEST')
    print('TLC: Tunnel Low Capacity (Kbps)')
    print('THC: Tunnel High Capacity (Kbps)')
    print('SM: Selective Mode (> 0 e < 1)')
    print('IFP: Input File Path')
    print('TEST: ')
    print('  - FA: Original VGuard Dynamic Flow Allocation')
    print('  - FAS: Adapted VGuard Dynamic Flow Allocation')
    print('  - DOUBLE: FA and FAS')
    print('==========================================================')

if len(sys.argv) != 6:
    print('ERROR: WRONG ARGUMENTS AMOUNT')
    help()
    exit(-1)
TLC = int(sys.argv[1])
if TLC <= 0:
    print('ERROR: TUNNEL LOW CAPACITY MUST BE > 0')
    help()
    exit(-1)
THC = int(sys.argv[2])
if THC <= 0:
    print('ERROR: TUNNEL HIGH CAPACITY MUST BE > 0')
    help()
    exit(-1)
SM = float(sys.argv[3])
if SM <= 0 or SM >= 1:
    print('ERROR: TUNNEL HIGH SELECTIVITY MODE MUST BE > 0 AND < 1')
    help()
    exit(-1)
IFP = sys.argv[4]
if not path.isfile(IFP):
    print('ERROR: INPUT FILE DOES NOT EXISTS')
    help()
    exit(-1)
TEST = sys.argv[5]
if TEST != 'FA' and TEST != 'FAS' and TEST != 'DOUBLE':
    print('ERROR: TEST TYPE DOES NOT EXISTS')
    help()
    exit(-1)

simulator = MethodsSimulator()
if TEST == 'FA' or TEST == 'DOUBLE':
    print('=========================== ORIGINAL VGUARD TEST START ==========================\n')
    simulator.simulationBySecond(IFP, VGuardFA(TLC, THC, SM))
    print('============================ ORIGINAL VGUARD TEST END ===========================')
if TEST == 'FAS' or TEST == 'DOUBLE':
    print('============================ ADAPTED VGUARD TEST START ==========================\n')
    simulator.simulationBySecond(IFP, VGuardFAS(TLC, THC, SM))
    print('============================= ADAPTED VGUARD TEST END ===========================')