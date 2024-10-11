#ifndef SIMULATED_ANNEALING_H
#define SIMULATED_ANNEALING_H

#include "function/array.h"
#include "function/magic_cube.h"

magiccube simulated_annealing_value(magiccube initial_cube, double (*objective_function)(magiccube), double (*temperature_function)(double), double T);
magiccube simulated_annealing_cost(magiccube initial_cube, double (*objective_function)(magiccube), double (*temperature_function)(double), double T);
double division_temperature_function(double T);

#endif