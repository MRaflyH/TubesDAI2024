#ifndef RANDOM_RESTART_HILL_CLIMBING_H
#define RANDOM_RESTART_HILL_CLIMBING_H

#include "function/array.h"
#include "function/magic_cube.h"

magiccube random_restart_hill_climbing_value(double (*value_function)(magiccube), int max_iteration);
magiccube random_restart_hill_climbing_cost(double (*cost_function)(magiccube), int max_iteration);

#endif