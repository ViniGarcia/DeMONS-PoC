DeMONS: DDoS MitigatiOn NFV Solution
========================================================

*Status: Stable -- Version: 1.0*

### What is DeMONS?

DeMONS is a DDoS mitigation solution that uses NFV concept together both a dynamic allocation and a reputation mechanisms. This repository provides a DeMONS simulator for measuring satisfaction (i.e., a QoS metric calculated by using the traffic drop rate and flows priorities) in differente traffic scenarios. In addition to the DeMONS simulator, we also provide a VGuard solution simulator [1] to be used as the baseline for comparison. <br/>

The DeMONS simulator can be controlled by its CLI (CLI.py). This interface provides five actions as described below:<br/>
<br/>
flow -> create a simulation flow summary<br/>
- arguments for normal flows: file distribution<br/>
- arguments for DDoS flows: file benign_distribution ddos_distribution ddos_start_moment<br/>
-- file: string (file where the data will be written)<br/>
-- distributions: N100/30-1, N100/30-2, N500/30, D500/10 (data distribution equation)<br/>
-- ddos_start_moment: integer (time when the DDoS starts)(<br/>
<br/>
vguard -> execute a VGuard solution simulation<br/>
- arguments: flow_file tunnel_low_cap tunnel_high_cap selective_mode<br/>
-- flow_file: string (flow file formatted as the one created by flow action)<br/>
-- tunnel_low_cap: integer (capacity of low priority tunnel in Kbps)<br/>
-- tunnel_high_cap: integer (capacity of high priority tunnel in Kbps)<br/>
-- selective_mode: float (>= 0 and <= 1) (selective mode entrance parameter)<br/>
<br/>
demons -> execute a DeMONS solution simulation<br/>
- arguments: flow_file tunnel_low_cap tunnel_high_cap selective_mode<br/>
-- flow_file: string (flow file formatted as the one created by flow action)<br/>
-- tunnel_low_cap: integer (capacity of low priority tunnel in Kbps)<br/>
-- tunnel_high_cap: integer (capacity of high priority tunnel in Kbps)<br/>
-- selective_mode: float (>= 0 and <= 1) (selective mode entrance parameter)<br/>
<br/>
full -> execute both VGuad and DeMONS simulations<br/>
- arguments: flow_file tunnel_low_cap tunnel_high_cap selective_mode<br/>
-- flow_file: string (flow file formatted as the one created by flow action)<br/>
-- tunnel_low_cap: integer (capacity of low priority tunnel in Kbps)<br/>
-- tunnel_high_cap: integer (capacity of high priority tunnel in Kbps)<br/>
-- selective_mode: float (>= 0 and <= 1) (selective mode entrance parameter)<br/>
<br/>
exit -> end simulator<br/>

The NIEP platform was developed using python 2.7 language.

### Next Steps

1. Real environment deployment and testing (Click-on-OSv [2] in NIEP [3] environment).
2. Dynamic setup of selective mode parameter.

### Support

Contact us towards git issues requests or by the e-mail vfulber@inf.ufsm.br.

### DeMONS Research Group

Vinícius Fülber Garcia (vfulber@inf.ufsm.br) - UFSM, Brazil <br/>
Guilherme de Freitas Gaiardo (ggaiardo@inf.ufsm.br) - UFSM, Brazil <br/>
Raul Ceretta Nunes (ceretta@inf.ufsm.br) - UFSM, Brazil <br/>
Carlos Raniery Paula dos Santos (csantos@inf.ufsm.br) - UFSM, Brazil <br/>

### Publications

V. F. Garcia et al., "Uma Solução para Mitigação de Ataques DDoS Através de Tecnologia NFV", 2018 1st Workshop de Segurança Cibernética em Dispositivos Conectados (WSCDC SBRC). Campos do Jordão, Brazil, 2018.
<br/>
V. Fülber Garcia, G. de Freitas Gaiardo, L. da Cruz Marcuzzo, R. Ceretta Nunes and C. R. Paula dos Santos, "DeMONS: A DDoS Mitigation NFV Solution," 2018 IEEE 32nd International Conference on Advanced Information Networking and Applications (AINA), Krakow, 2018, pp. 769-776. doi: 10.1109/AINA.2018.00115

### References

-> VGuard <-<br/>
[1] C. J. Fung and B. McCormick, "VGuard: A distributed denial of service attack mitigation method using network function virtualization," 2015 11th International Conference on Network and Service Management (CNSM), Barcelona, Spain, 2015, pp. 64-70. doi:10.1109/CNSM.2015.7367340
<br/>
-> Click-On-OSv <-<br/>
[2] L. da Cruz Marcuzzo et al., "Click-on-OSv: A platform for running Click-based middleboxes", 2017 IFIP/IEEE Symposium on Integrated Network and Service Management (IM), Lisbon, 2017, pp. 885-886. doi: 10.23919/INM.2017.7987396
<br/>
-> NIEP <-<br/>
[3] T. Tavares, L. Marcuzzo, V. Garcia, G. Venâncio, M. Franco, L. Bondan, F. De Turk, L. Granville, E. Duarte, C. Santos and A. Schaeffer-filho, "NIEP - NFV Infrastructure Emulation Platform", in 32nd IEEE AINA, Cracow, Poland, 2018.
