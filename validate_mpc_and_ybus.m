clear;
define_constants;

mpc_c2m = Total_MG_casefile();
mpc_py = Total_MG_T1_python();


bkey = mpc_c2m.branch;
bmy = mpc_py.branch;

% map my bus numbers to key bus numbers
bus_map = [1 2 3 4 5 6 7 8 10 9 11 12 13 14 15 16 17];

bus_rearrange = [7 14 9 12 8 1 3 6 2 10 5 16 11 13 4 15];

bmy(:,F_BUS) = bus_map(bmy(:,F_BUS));
bmy(:,T_BUS) = bus_map(bmy(:,T_BUS));

for i=1:size(bkey,1)
    bus1 = bkey(i,F_BUS);
    bus2 = bkey(i,T_BUS);
    
    for j=1:size(bmy,1)
        if (bus1 == bmy(j,T_BUS) && bus2 == bmy(j,F_BUS)) || ...
           (bus2 == bmy(j,T_BUS) && bus1 == bmy(j,F_BUS))
            idx(i) = j;
        end
    end
end

idx;
    
bmy(:,[BR_R BR_X BR_B]) == bkey(:,[BR_R BR_X BR_B]);


%% Compare python pf with cim2matpower pf
mpc_c2m = runpf(mpc_c2m,mpoption('verbose',0,'out.all',0));
mpc_py = runpf(mpc_py,mpoption('verbose',0,'out.all',-1));

disp('Angle magnitude differences:')
[mpc_py.bus(bus_rearrange,[BUS_I VA VM]) mpc_c2m.bus(:,[BUS_I VA VM])];

max([mpc_py.bus(bus_rearrange,VM) - mpc_c2m.bus(:,VM)])

%% Compare Ybuses 
% Build Y-bus with matpower
Ymatpower = makeYbus(ext2int(mpc_py));
% Get Y-bus from python
Total_MG_T1_Ybus;

disp('Y bus difference:')
max(max(abs([Y-Ymatpower])))