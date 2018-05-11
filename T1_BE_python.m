function mpc = T1_BE_python

mpc.baseMVA = 100;

mpc.bus = [
1	1	0    	0   	1.0108	49.9624 	1	1	0	380.0	1	1.1	0.9
2	1	1.0  	0.0 	0     	0       	1	1	0	225.0	1	1.1	0.9
3	1	200.0	50.0	0     	0       	1	1	0	225.0	1	1.1	0.9
4	3	0    	0   	0     	0       	1	1	0	10.5 	1	1.1	0.9
5	1	200.0	90.0	0.0   	299.9953	1	1	0	110.0	1	1.1	0.9
];

mpc.branch = [
3	2	0.0038222222222222225	0.06755555555555556 	0.021470821875       	0	0	0	1	0	1	-360	360
3	2	0.010277530864197531 	0.1402469135802469  	0.010131024375       	0	0	0	1	0	1	-360	360
5	1	0.0018751329639889198	0.010054642659279777	0.0                  	0	0	0	1	0	1	-360	360
5	3	0.0016252839506172838	0.02200273185185185 	0.0                  	0	0	0	1	0	1	-360	360
4	5	0.0008653801652892561	0.04829271900826446 	-0.010047101899999999	0	0	0	1	0	1	-360	360
];

mpc.gen = [
4	90.0	100.256	0	0	1	100	1	90.0	0
];

