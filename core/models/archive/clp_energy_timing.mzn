% DEBUG MODEL: ENERGY + TIMING CONSTRAINTS
% Tests if timing constraints cause infeasibility

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
int: mu;
int: psi;
int: SM;

array[B,1..max_stops] of int: D;
array[B,1..max_stops] of int: T;
array[B,1..max_stops] of int: tau_bi;

% Variables
array[B,1..max_stops] of var Cmin..Cmax: cbi;
array[B,1..max_stops] of var 0..Cmax: ebi;
array[B,1..max_stops] of var 0..600: ctbi;
array[B,1..max_stops] of var 0..3000: tbi;
array[B,1..max_stops] of var 0..500: d_tbi;
array[B,1..max_stops] of var 0..1: xbi;
array[ST] of var 0..1: xst;

% Initial conditions
constraint forall(b in B)(
    cbi[b,1] = Cmax /\
    tbi[b,1] = tau_bi[b,1]  % First bus starts on time
);

% Battery constraints
constraint forall(b in B, i in 1..num_stops[b]) (
    cbi[b,i] >= Cmin /\
    cbi[b,i] + ebi[b,i] <= Cmax /\
    alpha * ctbi[b,i] >= ebi[b,i]
);

% Battery evolution
constraint forall(b in B, i in 2..num_stops[b]) (
    cbi[b,i] <= cbi[b,i-1] + ebi[b,i-1] - D[b,i]
);

% Timing constraints
constraint forall(b in B, i in 2..num_stops[b]) (
    tbi[b,i] >= tbi[b,i-1] + ctbi[b,i-1] + T[b,i] /\
    tbi[b,i] >= tbi[b,i-1] + ctbi[b,i-1] + SM * xbi[b,i-1]
);

% Time deviation
constraint forall(b in B, i in 1..num_stops[b]) (
    d_tbi[b,i] >= tbi[b,i] - tau_bi[b,i] /\
    d_tbi[b,i] >= tau_bi[b,i] - tbi[b,i] /\
    d_tbi[b,i] <= mu /\
    ctbi[b,i] >= psi * xbi[b,i]
);

% Charger constraints
constraint forall(b in B, i in 1..num_stops[b])(
    xst[st_bi[b,i]] >= xbi[b,i]
);

% Minimum energy
constraint forall(b in B)(
    sum(i in 1..num_stops[b])(ebi[b,i]) >=
    sum(i in 1..num_stops[b])(D[b,i]) - Cmax + Cmin
);

solve minimize sum(st in ST)(xst[st]);

output [
  "STATUS: Energy + Timing model\n",
  "Battery: ", show(cbi), "\n",
  "Timing: ", show(tbi), "\n",
  "Deviation: ", show(d_tbi), "\n",
  "Stations: ", show(sum(s in ST)(xst[s])), "\n"
];
