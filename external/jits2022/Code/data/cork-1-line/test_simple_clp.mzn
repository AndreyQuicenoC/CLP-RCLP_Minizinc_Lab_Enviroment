% Minimal test model to debug the issue

int: num_buses = 2;
set of int: B = 1..num_buses;

int: num_stations = 5;
set of int: ST = 1..num_stations;

int: max_stops = 10;
array[B] of int: num_stops = [5, 4];

% Parameters
int: Cmax = 1000;
int: Cmin = 200;
int: alpha = 100;
int: mu = 5;
int: SM = 1;
int: psi = 1;
int: beta = 10;
int: M = 5000;

% Data
array[B,1..max_stops] of int: D = array2d(1..2, 1..10, [
  0, 1, 1, 1, 1, 0, 0, 0, 0, 0,  % Bus 1
  0, 1, 1, 1, 0, 0, 0, 0, 0, 0   % Bus 2
]);

array[B,1..max_stops] of int: T = array2d(1..2, 1..10, [
  0, 4, 2, 2, 2, 0, 0, 0, 0, 0,  % Bus 1
  0, 4, 2, 2, 0, 0, 0, 0, 0, 0   % Bus 2
]);

array[B,1..max_stops] of int: tau_bi = array2d(1..2, 1..10, [
  420, 424, 426, 428, 430, 0, 0, 0, 0, 0,  % Bus 1
  480, 484, 486, 488, 0, 0, 0, 0, 0, 0     % Bus 2
]);

array[B,1..max_stops] of int: st_bi = array2d(1..2, 1..10, [
  1, 2, 3, 4, 5, 1, 1, 1, 1, 1,  % Bus 1
  1, 2, 3, 4, 1, 1, 1, 1, 1, 1   % Bus 2
]);

% Variables
array[B,1..max_stops] of var 0..1600: cbi;
array[B,1..max_stops] of var 0..1600: ebi;
array[B,1..max_stops] of var 0..600: ctbi;
array[B,1..max_stops] of var 0..3000: tbi;
array[B,1..max_stops] of var 0..500: d_tbi;
array[B,1..max_stops] of var 0..1: xbi;
array[ST] of var 0..1: xst;

% Constraints
constraint forall(b in B) (cbi[b,1] = Cmax);

constraint forall(b in B, i in 1..num_stops[b]) (
    cbi[b,i] >= Cmin /\
    cbi[b,i] + ebi[b,i] <= Cmax /\
    alpha * ctbi[b,i] >= ebi[b,i]
);

constraint forall(b in B, i in 2..num_stops[b]) (
    cbi[b,i] <= cbi[b,i-1] + ebi[b,i-1] - D[b,i]
);

constraint forall(b in B, i in 2..num_stops[b]) (
    tbi[b,i] >= tbi[b,i-1] + ctbi[b,i-1] + T[b,i] /\
    tbi[b,i] >= tbi[b,i-1] + ctbi[b,i-1] + SM * xbi[b,i-1]
);

constraint forall(b in B, i in 1..num_stops[b]) (
    d_tbi[b,i] >= tbi[b,i] - tau_bi[b,i] /\
    d_tbi[b,i] >= tau_bi[b,i] - tbi[b,i] /\
    d_tbi[b,i] <= mu /\
    ctbi[b,i] >= psi * xbi[b,i]
);

constraint forall(b in B, i in 1..num_stops[b]) (
    beta * xbi[b,i] >= ctbi[b,i] /\
    xst[st_bi[b,i]] >= xbi[b,i]
);

constraint forall(b in B)(
    sum(i in 1..num_stops[b])(ebi[b,i]) >=
    sum(i in 1..num_stops[b])(D[b,i]) - Cmax + Cmin
);

constraint forall(b in B, i in num_stops[b]+1..max_stops) (
    cbi[b,i] = 0 /\
    ebi[b,i] = 0 /\
    ctbi[b,i] = 0 /\
    tbi[b,i] = 0 /\
    d_tbi[b,i] = 0 /\
    xbi[b,i] = 0
);

solve minimize sum(s in ST)(xst[s]);

output [
  "Estaciones: ", show(xst), "\n",
  "Total: ", show(sum(s in ST)(xst[s])), "\n"
];
