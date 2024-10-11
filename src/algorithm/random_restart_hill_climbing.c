#include "random_restart_hill_climbing.h"

magiccube random_restart_hill_climbing_value(double (*objective_function)(magiccube), int max_iteration) {
    magiccube current_cube, next_cube, best_cube;
    double current_value, best_value;
    best_cube = random_magic_cube();
    best_value = objective_function(best_cube);
    int i = 0;
    while (i < max_iteration && best_value < 109) {
        printf("\r%d / %d", i, max_iteration);
        fflush(stdout);
        current_cube = random_magic_cube();
        while (1) {
            next_cube = steepest_neighbor_value(current_cube, objective_function);
            if (objective_function(next_cube) <= objective_function(current_cube)) {
                free_cube(next_cube);
                break;
            }
            free_cube(current_cube);
            current_cube = next_cube;
        }
        current_value = objective_function(current_cube);
        if (current_value > best_value) {
            free_cube(best_cube);
            best_cube = current_cube;
            best_value = current_value;
        }
        else free(current_cube);
        i++;
        printf("\r%d / %d || value = %f", i, max_iteration, best_value);
        fflush(stdout);
    }
    printf("\n");
    return best_cube;
}

magiccube random_restart_hill_climbing_cost(double (*objective_function)(magiccube), int max_iteration) {
    magiccube current_cube, next_cube, best_cube;
    double current_cost, best_cost;
    best_cube = random_magic_cube();
    best_cost = objective_function(best_cube);
    int i = 0;
    while (i < max_iteration && best_cost > 0) {
        current_cube = random_magic_cube();
        while (1) {
            next_cube = steepest_neighbor_cost(current_cube, objective_function);
            if (objective_function(next_cube) >= objective_function(current_cube)) {
                free_cube(next_cube);
                break;
            }
            free_cube(current_cube);
            current_cube = next_cube;
        }
        current_cost = objective_function(current_cube);
        if (current_cost < best_cost) {
            free_cube(best_cube);
            best_cube = current_cube;
            best_cost = current_cost;
        }
        else free(current_cube);
        i++;
        printf("\r%d / %d || cost = %f", i, max_iteration, best_cost);
        fflush(stdout);
    }
    printf("\n");
    return best_cube;
}