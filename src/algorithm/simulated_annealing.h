#ifndef SIMULATED_ANNEALING_H
#define SIMULATED_ANNEALING_H

#include "function/array.h"
#include "function/magic_cube.h"
#include <float.h>

magiccube simulated_annealing_value(magiccube initial_cube, double (*value_function)(magiccube), double (*temperature_function)(double), double temperature);
magiccube simulated_annealing_cost(magiccube initial_cube, double (*cost_function)(magiccube), double (*temperature_function)(double), double temperature);
double geometric_temperature_function(double temperature);
double arithmatic_temperature_function(double temperature);
double lm_temperature_function(double temperature);
int decision(double probability);

#endif