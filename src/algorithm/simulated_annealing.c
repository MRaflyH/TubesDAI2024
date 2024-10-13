#include "simulated_annealing.h"

magiccube simulated_annealing_value(magiccube initial_cube, double (*value_function)(magiccube), double (*temperature_function)(double), double temperature) {
    int i = 0;
    magiccube current_cube;
    double current_value, next_value, de;
    int cube_index_1, cube_index_2;
    current_cube = deep_copy_magic_cube(initial_cube);
    current_value = value_function(current_cube);
    while (temperature > 0 && current_value < 109) {
        cube_index_1 = random_int(125);
        cube_index_2 = random_int(125);
        while (cube_index_1 == cube_index_2) {
            cube_index_1 = random_int(125);
            cube_index_2 = random_int(125);
        }
        cube_swap(current_cube, cube_index_1, cube_index_2);
        next_value = value_function(current_cube);
        de = next_value - current_value;
        // de = -1;
        if (de > 0 || decision(exp(de/temperature))) current_value = next_value;
        else cube_swap(current_cube, cube_index_1, cube_index_2);
        // if (exp(de/temperature) > 0.99999999)
        printf("\ntemp = %.5f || value = %f || probability = %f || de = %f || i = %d", temperature, current_value, exp(de/temperature), de, i);
        // printf("\n\n\n%d temp = %.308f", i, temperature);
        fflush(stdout);
        temperature = temperature_function(temperature);
        i++;
    }
    printf("\n");
    return current_cube;
}

magiccube simulated_annealing_cost(magiccube initial_cube, double (*cost_function)(magiccube), double (*temperature_function)(double), double temperature) {
    int i = 0;
    magiccube current_cube;
    double current_cost, next_cost, de;
    int cube_index_1, cube_index_2;
    current_cube = deep_copy_magic_cube(initial_cube);
    current_cost = cost_function(current_cube);
    while (temperature > 0 && current_cost > 0) {
        cube_index_1 = random_int(125);
        cube_index_2 = random_int(125);
        while (cube_index_1 == cube_index_2) {
            cube_index_1 = random_int(125);
            cube_index_2 = random_int(125);
        }
        cube_swap(current_cube, cube_index_1, cube_index_2);
        next_cost = cost_function(current_cube);
        de = current_cost - next_cost;
        // de = -1;
        if (de > 0 || decision(exp(de/temperature))) current_cost = next_cost;
        else cube_swap(current_cube, cube_index_1, cube_index_2);
        // if (exp(de/temperature) > 0.000001 && exp(de/temperature) < 0.9)
        // printf("\ntemp = %.5f || cost = %f || probability = %f || de = %f || i = %d", temperature, current_cost, exp(de/temperature), de, i);
        // printf("\n\n\n%d temp = %.308f", i, temperature);
        // fflush(stdout);
        temperature = temperature_function(temperature);
        i++;
    }
    // printf("\n");
    return current_cube;
}

double geometric_temperature_function(double temperature) {
    double new_t = temperature*0.999;
    if (new_t <= DBL_MIN) {
        new_t = 0;
    }
    return new_t;
}

double arithmatic_temperature_function(double temperature) {
    double new_t = temperature-0.1;
    if (new_t <= 0) {
        new_t = 0;
    }
    return new_t;
}

double lm_temperature_function(double temperature) {
    double new_t = temperature / (1 + 0.5 * temperature);
    if (new_t <= 0.00001) {
        new_t = 0;
    }
    return new_t;
}

int decision(double probability) {
    return random_int(1000000) < probability * 1000000;
}