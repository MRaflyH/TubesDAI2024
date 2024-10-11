#include "simulated_annealing.h"

magiccube simulated_annealing_value(magiccube initial_cube, double (*objective_function)(magiccube), double (*temperature_function)(double), double T) {
    magiccube current_cube, next_cube;
    return current_cube;
}

magiccube simulated_annealing_cost(magiccube initial_cube, double (*objective_function)(magiccube), double (*temperature_function)(double), double T);

double division_temperature_function(double T) {
    double new_T = T/2;
    if ((int)new_T == 0) {
        new_T = 0;
    }
    return new_T;
}
