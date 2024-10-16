#include "algorithm/genetic_algorithm.h"
#include "algorithm/random_restart_hill_climbing.h"
#include "algorithm/simulated_annealing.h"

int main() {
    clock_t t; 

    // 0 -> line value
    // 1 -> variance cost
    int obj_option = 1;

    // 0 -> geometric formula
    // 1 -> arithmatic formula
    int temp_option = 0;

    double (*objective)(magiccube);
    // magiccube (*genetic)();
    magiccube (*restart)(double(*)(magiccube), int);
    magiccube (*annealing)(magiccube, double(*)(magiccube), double(*)(double), double);
    double (*temperature_function)(double);

    switch (obj_option) {
        case 0:
            objective = line_objective_function;
            restart = random_restart_hill_climbing_value;
            annealing = simulated_annealing_value;
            break;
        case 1:
            objective = var_objective_function;
            restart = random_restart_hill_climbing_cost;
            annealing = simulated_annealing_cost;
            break;
        default:
            return 0;
    }
    
    switch (temp_option) {
        case 0:
            temperature_function = geometric_temperature_function;
        case 1:
            temperature_function = arithmatic_temperature_function;
    }
    
    // int solution[125] = {25,16,80,104,90,115,98,4,1,97,42,111,85,2,75,66,72,27,102,48,67,18,119,106,5,91,77,71,6,70,52,64,117,69,13,30,118,21,123,23,26,39,92,44,114,116,17,14,73,95,47,61,45,76,86,107,43,38,33,94,89,68,63,58,37,32,93,88,83,19,40,50,81,65,79,31,53,112,109,10,12,82,34,87,100,103,3,105,8,96,113,57,9,62,74,56,120,55,49,35,121,108,7,20,59,29,28,122,125,11,51,15,41,124,84,78,54,99,24,60,36,110,46,22,101};
    
    // randomise seed
    srand(time(NULL));
    rand();

    // magiccube mySolution;
    // mySolution = create_magic_cube(solution);
    // magiccube myCube;
    // myCube = random_magic_cube();
    // display_cube(myCube);

    // magiccube neighborCube;
    // neighborCube = random_neighbor(myCube);
    // display_cube(neighborCube);

    // magiccube restartCube;
    // restartCube = restart(objective, 10);
    // display_cube(restartCube);

    magiccube annealingCube;
    // annealingCube = simulated_annealing_cost(myCube, objective, geometric_temperature_function, 1000000000);
    // printf("%f\n%f\n", var_objective_function(annealingCube), line_objective_function(annealingCube));
    // display_cube(annealingCube);


    t = clock(); 
    double cost = 0;
    double line = 0;
    double time = 0;
    
    for (int i = 0; i < 100; i++) {
        t = clock(); 
        annealingCube = annealing(random_magic_cube(), var_objective_function, geometric_temperature_function, 1000000000);
        t = clock() - t; 
        time += ((double)t)/CLOCKS_PER_SEC; 
        cost += var_objective_function(annealingCube);
        line += line_objective_function(annealingCube);
        printf("\r%d", i);
        fflush(stdout);
    }
    printf("\n");
    printf("avg cost = %f\n", cost/100);
    printf("avg line = %f\n", line/100);
    printf("avg time = %f\n", time/100);

    // t = clock() - t; 
    // double time_taken = ((double)t)/CLOCKS_PER_SEC; // in seconds 
    // printf("%f seconds\n", time_taken); 

    return 0;
}