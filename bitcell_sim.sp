* bitcell simulation 
* .lib "/gpfs/gibbs/pi/manohar/tech/SKY/130/skywater-pdk/libraries/sky130_fd_pr/latest/models/sky130.lib.spice" 
.lib "/gpfs/gibbs/project/manohar/mdd42/sky130_fd_pr_copy/latest/models/sky130.lib.spice" ff 
.global Vdd GND Q Q_
.include bitcell_array_1x1_sky130.sp
*.option post
*.finesim_output=tr0
.param MC_SWITCH=1
*.model smod VSWITCH(RON=0.1m, VON=0, ROFF=10MEG, VOFF=1.8)


VDD Vdd GND 1.8
VGND GND 0 0 

* write margin setup 
* .ic bl=0 bl_=1.8
* VWL wl GND 1.8
* VBL bl GND 0 
* VQ Q GND 0


* read margin setup
* .ic bl=1.8 bl_=1.8
* VWL wl GND 1.8
* VBL bl GND 1.8 
* VBL_ bl_ GND 1.8
* VQ Q GND 0

* read margin setup
VWL wl GND 1.8 
VBL bl GND 1.8
VBL_ bl_ GND 1.8

* voltage at switch 1
VQ N GND  pwl 0ms 0 1ms 0 2ms 1.8
* control for first swtich 
VC1 C1 GND pwl  2ms 1.8 2.001ms 0
* voltage controlled switch
G1 Q N VCR pwl(1) C1 GND 0, 100MEG, 1.8, 0.0

* voltage at swtich 2 
VQ_ N_ GND pwl 0ms 1.8 4ms 1.8 5ms 0
* control for second switch
VC2 C2 GND pwl 0ms 0 3ms 0 3.001ms 1.8 5ms 1.8 5.001ms 0
* voltage controlled switch
G2 Q_ N_ VCR pwl(1) C2 GND 0, 100MEG, 1.8, 0.0


XB1 wl bl bl_ ::mem::bitcell

.tran 0.01ms 6ms strobeperiod=0.001ms SWEEP MONTE=5


.print TRAN  V(Q) V(Q_) 
.end


