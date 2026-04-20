% DEBUG MODEL: ENERGY CONSTRAINTS ONLY
% Tests if energy feasibility works in isolation

int: num_buses;
set of int: B = 1..num_buses;

int: num_stations;
set of int: ST = 1..num_stations;

int: max_stops;
array[B] of int: num_stops;
array[B,1..max_stops] of int: st_bi;

int: Cmax;
int: Cmin;
int: alpha;
int: mu;  % Include all parameters used in data
int: psi;
int: SM;

array[B,1..max_stops] of int: D;
array[B,1..max_stops] of int: T;
array[B,1..max_stops] of int: tau_bi;

% Variables
array[B,1..max_stops] of var Cmin..Cmax: cbi;
array[B,1..max_stops] of var 0..Cmax: ebi;
array[B,1..max_stops] of var 0..1: xbi;
array[ST] of var 0..1: xst;

% Initial battery condition
constraint forall(b in B)(
    cbi[b,1] = Cmax
);

% Battery constraints
constraint forall(b in B, i in 1..num_stops[b]) (
    cbi[b,i] >= Cmin /\
    cbi[b,i] + ebi[b,i] <= Cmax /\
    alpha * 600 >= ebi[b,i]  % max charging time = 600 min
);

% Battery evolution
constraint forall(b in B, i in 2..num_stops[b]) (
    cbi[b,i] <= cbi[b,i-1] + ebi[b,i-1] - D[b,i]
);

% Minimum energy requirement
constraint forall(b in B)(
    sum(i in 1..num_stops[b])(ebi[b,i]) >=
    sum(i in 1..num_stops[b])(D[b,i]) - Cmax + Cmin
);

% Charger installation
constraint forall(b in B, i in 1..num_stops[b])(
    xst[st_bi[b,i]] >= xbi[b,i]
);

solve minimize sum(st in ST)(xst[st]);

output [
  "STATUS: Energy-only model\n",
  "Battery levels: ", show(cbi), "\n",
  "Charging amounts: ", show(ebi), "\n",
  "Stations: ", show(sum(s in ST)(xst[s])), "\n"
];
