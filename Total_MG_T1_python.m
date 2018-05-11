function mpc = Total_MG_T1_python

mpc.baseMVA = 100;

mpc.bus = [
1 	1	0    	0    	1.0108	49.9624           	1	1    	0	380.0	1	1.1	0.9
2 	1	1.0  	0.0  	0     	0                 	1	1    	0	225.0	1	1.1	0.9
3 	1	200.0	50.0 	0     	0                 	1	1    	0	225.0	1	1.1	0.9
4 	2	0    	0    	0     	0                 	1	1    	0	10.5 	1	1.1	0.9
5 	1	0    	0    	0     	0                 	1	1    	0	21.0 	1	1.1	0.9
6 	1	200.0	90.0 	0.0   	299.9953          	1	1    	0	110.0	1	1.1	0.9
7 	1	486.0	230.0	0     	0                 	1	1    	0	220.0	1	1.1	0.9
8 	2	0    	0    	0     	0                 	1	1.017	0	15.75	1	1.1	0.9
9 	1	100.0	290.0	0.0   	50.080000000000005	1	1    	0	400.0	1	1.1	0.9
10	3	0    	0    	0     	0                 	1	1.018	0	15.75	1	1.1	0.9
11	1	0.0  	0.0  	0     	0                 	1	1    	0	380.0	1	1.1	0.9
12	1	0.0  	0.0  	0     	0                 	1	1    	0	380.0	1	1.1	0.9
14	1	0.0  	0.0  	0     	0                 	1	1    	0	380.0	1	1.1	0.9
15	1	0.0  	0.0  	0     	0                 	1	1    	0	220.0	1	1.1	0.9
16	1	0.0  	0.0  	0     	0                 	1	1    	0	220.0	1	1.1	0.9
17	1	0    	0    	0     	0                 	1	1    	0	380.0	1	1.1	0.9
];

mpc.branch = [
15	2 	0.004345679012345679  	0.13471604938271606  	0.0419873625         	0	0	0	1	0	1	-360	360
3 	2 	0.0038222222222222225 	0.06755555555555556  	0.021470821875       	0	0	0	1	0	1	-360	360
1 	11	0.0007271468144044322 	0.008310249307479225 	0.216389176          	0	0	0	1	0	1	-360	360
1 	14	0.00016620498614958447	0.0013850415512465374	0.0363824464         	0	0	0	1	0	1	-360	360
1 	12	0.00029085872576177285	0.004362880886426592 	0.0952655896         	0	0	0	1	0	1	-360	360
3 	2 	0.010277530864197531  	0.1402469135802469   	0.010131024375       	0	0	0	1	0	1	-360	360
16	2 	0.00908641975308642   	0.1362962962962963   	0.010973981249999999 	0	0	0	1	0	1	-360	360
9 	11	0.0006375             	0.0075               	0.22619472           	0	0	0	1	0	1	-360	360
9 	14	0.00145               	0.01265              	0.04021232           	0	0	0	1	0	1	-360	360
7 	16	0.010454545454545454  	0.14256198347107438  	0.009792239599999999 	0	0	0	1	0	1	-360	360
7 	15	0.004545454545454546  	0.13636363636363635  	0.043487158          	0	0	0	1	0	1	-360	360
9 	12	0.0002625             	0.0039375            	0.10379823999999999  	0	0	0	1	0	1	-360	360
6 	1 	0.0018751329639889198 	0.010054642659279777 	0.0                  	0	0	0	1	0	1	-360	360
6 	3 	0.0016252839506172838 	0.02200273185185185  	0.0                  	0	0	0	1	0	1	-360	360
4 	6 	0.0008653801652892561 	0.04829271900826446  	-0.010047101899999999	0	0	0	1	0	1	-360	360
17	1 	0.0006222036011080332 	0.011914216066481995 	0.00351975           	0	0	0	1	0	1	-360	360
17	3 	0.0002243130193905817 	0.0041198656509695295	0.0                  	0	0	0	1	0	1	-360	360
17	5 	9.232686980609419e-06 	4.153601108033241e-05	0.0                  	0	0	0	1	0	1	-360	360
7 	9 	0.0008437500000000001 	0.0174796475         	-0.007111200000000001	0	0	0	1	0	1	-360	360
8 	7 	0.00014285743801652892	0.01111019214876033  	-0.0687389868        	0	0	0	1	0	1	-360	360
10	7 	0.00013492148760330577	0.011110291322314048 	-0.0687389868        	0	0	0	1	0	1	-360	360
];

mpc.gen = [
4 	90.0      	100.256   	0	0	1    	100	1	90.0      	0
10	600.492701	386.922556	0	0	1.018	100	1	600.492701	0
8 	140.0     	77.743    	0	0	1.017	100	1	140.0     	0
8 	150.0     	83.296    	0	0	1.017	100	1	150.0     	0
];

