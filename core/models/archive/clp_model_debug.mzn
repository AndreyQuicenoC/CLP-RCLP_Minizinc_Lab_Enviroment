% SIMPLIFIED MODEL FOR DEBUGGING
% Only energy constraints, no timing constraints

int: num_buses;
set of int: B = 1..num_buses;

int: num_stations;
set of int: ST = 1..num_stations;

int: max_stops;
array[B] of int: num_stops;
array[B,1..max_stops] of int: st_bi;
array[B,1..max_stops] of int: D;
array[B,1..max_stops] of int: T;
array[B,1..max_stops] of int: tau_bi;

int: Cmax;
int: Cmin;
int: alpha;

% Decision variables
array[B,1..max_stops] of var Cmin..Cmax: cbi;   % Battery level
array[B,1..max_stops] of var 0..Cmax: ebi;      % Charge amount
array[B,1..max_stops] of var 0..1: xbi;         % Charge yes/no
array[ST] of var 0..1: xst;                     % Station installed

% Initial battery
constraint forall(b in B)(
    cbi[b,1] = Cmax
);

% Battery evolution
constraint forall(b in B, i in 2..num_stops[b]) (
    cbi[b,i] <= cbi[b,i-1] + ebi[b,i-1] - D[b,i]
);

% Energy constraint
constraint forall(b in B)(
    sum(i in 1..num_stops[b])(ebi[b,i]) >= sum(i in 1..num_stops[b])(D[b,i]) - Cmax + Cmin
);

% Charging constraint
constraint forall(b in B, i in 1..num_stops[b])(
    ebi[b,i] <= Cmax - cbi[b,i]
);

% Minimize stations
solve minimize sum(st in ST)(xst[st]);

output [
  "Battery levels: ", show(cbi), "\n",
  "Charges: ", show(ebi), "\n",
  "Status: SAT\n"
];
