% ===== CLP MODEL - FLEXIBLE VERSION =====
% Supports both real-world data (relaxed timing) and generated instances (strict constraints)
% KEY CHANGE: Added 'strict_timing' parameter to control temporal constraint enforcement

% ----- PARÁMETROS DEL PROBLEMA -----

int: num_buses;
set of int: B = 1..num_buses;

int: num_stations;
set of int: ST = 1..num_stations;

int: max_stops;
array[B] of int: num_stops;
array[B,1..max_stops] of int: st_bi;

% ----- ESCALA NUMÉRICA -----

int: SCALE = 10;

% ----- CONSTANTES DEL MODELO -----

int: Cmax;
int: Cmin;
int: alpha;
int: mu;
int: SM;
int: psi;
int: beta;
int: M;

% ----- CONTROL PARAMETERS -----
int: strict_timing = 1;  % 0=relax timing for real data, 1=strict for generated

% ----- DATOS DE LAS RUTAS -----

array[B,1..max_stops] of int: D;
array[B,1..max_stops] of int: T;
array[B,1..max_stops] of int: tau_bi;

% ----- VARIABLES DE DECISIÓN -----

array[B,1..max_stops] of var 0..1600: cbi;
array[B,1..max_stops] of var 0..1600: ebi;
array[B,1..max_stops] of var 0..600: ctbi;
array[B,1..max_stops] of var 0..3000: tbi;
array[B,1..max_stops] of var 0..500: d_tbi;

array[B,1..max_stops] of var 0..1: xbi;
array[ST] of var 0..1: xst;

array[B,B,1..max_stops,1..max_stops] of var 0..1: Zbdij;
array[B,B,1..max_stops,1..max_stops] of var 0..1: zbdi;

% ----- A. CAPACIDAD DE BATERÍA -----

constraint forall(b in B) (
    cbi[b,1] = Cmax
);

constraint forall(b in B, i in 1..num_stops[b]) (
    cbi[b,i] >= Cmin /\
    cbi[b,i] + ebi[b,i] <= Cmax /\
    alpha * ctbi[b,i] >= ebi[b,i]
);

constraint forall(b in B, i in 2..num_stops[b]) (
    cbi[b,i] <= cbi[b,i-1] + ebi[b,i-1] - D[b,i]
);

% ----- B. RESTRICCIONES DE TIEMPO -----

% Tiempo de llegada considerando viaje y carga
constraint forall(b in B, i in 2..num_stops[b]) (
    tbi[b,i] >= tbi[b,i-1] + ctbi[b,i-1] + T[b,i] /\
    tbi[b,i] >= tbi[b,i-1] + ctbi[b,i-1] + SM * xbi[b,i-1]
);

% Cálculo de desviación - FLEXIBLE según strict_timing
% Si strict_timing=1: Enforce d_tbi <= mu (original CLP)
% Si strict_timing=0: Allow deviation, only minimize (for real-world data)
constraint forall(b in B, i in 1..num_stops[b]) (
    d_tbi[b,i] >= tbi[b,i] - tau_bi[b,i] /\
    d_tbi[b,i] >= tau_bi[b,i] - tbi[b,i]
);

% CONDITIONAL: Only enforce mu limit if strict_timing=1
constraint forall(b in B, i in 1..num_stops[b] where strict_timing = 1) (
    d_tbi[b,i] <= mu
);

constraint forall(b in B, i in 1..num_stops[b]) (
    ctbi[b,i] >= psi * xbi[b,i]
);

% ----- C. INSTALACIÓN DE CARGADORES -----

constraint forall(b in B, i in 1..num_stops[b]) (
    beta * xbi[b,i] >= ctbi[b,i] /\
    xst[st_bi[b,i]] >= xbi[b,i]
);

% ----- D. NO SOLAPAMIENTO DE CARGAS -----

constraint forall(b,d in B where b < d)(
    forall(i in 1..num_stops[b], j in 1..num_stops[d]
    where st_bi[b,i] == st_bi[d,j])(

        Zbdij[b,d,i,j] <= xbi[b,i] /\
        Zbdij[b,d,i,j] <= xbi[d,j] /\
        xbi[b,i] + xbi[d,j] <= Zbdij[b,d,i,j] + 1 /\

        tbi[b,i] >= tbi[d,j] + ctbi[d,j] + SM - M * zbdi[b,d,i,j] /\
        tbi[d,j] >= tbi[b,i] + ctbi[b,i] + SM - M * zbdi[d,b,j,i] /\

        zbdi[b,d,i,j] + zbdi[d,b,j,i] - (1 - Zbdij[b,d,i,j]) <= 1
    )
);

% ----- E. ENERGÍA MÍNIMA REQUERIDA -----

constraint forall(b in B)(
    sum(i in 1..num_stops[b])(ebi[b,i]) >=
    sum(i in 1..num_stops[b])(D[b,i]) - Cmax + Cmin
);

% ----- F. FUNCIÓN OBJETIVO -----

% Minimize stations, with secondary objective to minimize deviation if not strict
solve minimize sum(st in ST)(xst[st]) + (1 - strict_timing) * sum(b in B, i in 1..max_stops)(d_tbi[b,i]) / 1000;

% ----- SALIDA DE RESULTADOS -----

output [
"Estaciones instaladas: ", show(sum(s in ST)(xst[s])), "\n",
"Total estaciones alcanzables: ", show(num_stations), "\n",
"Desviación totalen: ", show(sum(b in B, i in 1..max_stops)(d_tbi[b,i])), "\n",
"Modo temporal: ", if strict_timing = 1 then "STRICT (generated data)\n" else "RELAXED (real-world data)\n" endif
];
