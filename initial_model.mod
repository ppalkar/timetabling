# Declare sets
set TEAMS;                      # Set of teams
set TIMESLOTS;                  # Set of timeslots
set PROFESSORS;                 # Set of professors

# Define a set that links each professor to a set of teams
set Teams_per_prof {p in PROFESSORS} within TEAMS;

param maxTimeSlot;
param minTimeSlot;
param M;

# Declare the decision variables: 
var x {TEAMS, TIMESLOTS} binary; # x : Binary variable indicating if a team is assigned a particular timeslot


# var ymax {TEAMS} >= minTimeSlot, <= maxTimeSlot ;
# var ymin {TEAMS} >= minTimeSlot, <= maxTimeSlot ;


var tmax{PROFESSORS} >=minTimeSlot, <= maxTimeSlot ;
var tmin{PROFESSORS} >=minTimeSlot, <= maxTimeSlot ;


minimize Total_Gaps :
	sum{p in PROFESSORS}
		(tmax[p] - tmin[p]);

# Constraint: Each team is assigned exactly one timeslot
subject to OneTSlot {team in TEAMS}: sum {t in TIMESLOTS} x[team, t] == 1;

# Constraint: Each timeslot has exactly one team assigned
subject to OneTeam {t in TIMESLOTS}: sum {team in TEAMS} x[team, t] == 1;


# subject to Cymax {team in TEAMS, t in TIMESLOTS} : ymax[team] >= (t*x[team, t]);
# subject to Cymin {team in TEAMS, t in TIMESLOTS} : ymin[team] <= (t*x[team, t]) + M*(1-x[team, t]);

# subject to CProfMax{p in PROFESSORS, team in Teams_per_prof[p]} : tmax[p] >= ymax[team];
# subject to CProfMin{p in PROFESSORS, team in Teams_per_prof[p]} : tmin[p] <= ymin[team];



subject to CProfMax {p in PROFESSORS, team in Teams_per_prof[p], t in TIMESLOTS}:
 	tmax[p] >= (t * x[team, t]);

	
subject to CProfMin {p in PROFESSORS, team in Teams_per_prof[p], t in TIMESLOTS}:
	tmin[p] <= (t * x[team, t]) + (M*(1 - x[team, t])) ;


# subject to limit_ymax {team in TEAMS} : ymax[team] <= maxTimeSlot;
# subject to limit_ymin {team in TEAMS} : ymin[team] >= minTimeSlot;


# Constraint : setting bounds of tmin and tmax
 
subject to Ctmax {p in PROFESSORS} : tmax[p] <= maxTimeSlot;
subject to Ctmin {p in PROFESSORS} : tmin[p] >= minTimeSlot;




