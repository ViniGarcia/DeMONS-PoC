import sys
from os import path

sys.path.insert(0, '../Solutions/')
from VGuard import VGuard
from DeMONS import DeMONS

sys.path.insert(0, '../Simulators/')
from MethodsSimulator import MethodsSimulator

def help():
    print('=========================== HELP =========================')
    print('USAGE: python main.py TLC THC SM IFFP TEST')
    print('TLC: Tunnel Low Capacity (Kbps)')
    print('THC: Tunnel High Capacity (Kbps)')
    print('SM: Selective Mode (> 0 e < 1)')
    print('IFFP: Input Flow File Path')
    print('TEST: ')
    print('  - VGUARD: VGuard Dynamic Flow Allocation')
    print('  - DEMONS: DeMONS Dynamic Flow Allocation')
    print('  - DOUBLE: VGuard and DeMONS')
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
if TEST != 'VGUARD' and TEST != 'DEMONS' and TEST != 'DOUBLE':
    print('ERROR: TEST TYPE DOES NOT EXISTS')
    help()
    exit(-1)

simulator = MethodsSimulator()
if TEST == 'VGUARD' or TEST == 'DOUBLE':
    print('=========================== VGUARD TEST START ==========================\n')
    simulator.simulationBySecond(IFP, VGuard(TLC, THC, SM))
    print('============================ VGUARD TEST END ===========================')
if TEST == 'DEMONS' or TEST == 'DOUBLE':
    print('============================ DEMONS TEST START ==========================\n')
    simulator.simulationBySecond(IFP, DeMONS(TLC, THC, SM))
    print('============================= DEMONS TEST END ===========================')