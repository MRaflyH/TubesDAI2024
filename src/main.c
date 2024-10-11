#include "algorithm/genetic_algorithm.h"
#include "algorithm/random_restart_hill_climbing.h"
#include "algorithm/simulated_annealing.h"


int main() {

    // 0 -> line value
    // 1 -> standard deviation cost
    int obj_option = 0;

    // 0 -> division formula
    int temp_option = 0;

    double (*objective)(magiccube);
    // magiccube (*genetic)();
    magiccube (*restart)(double(*)(magiccube), int);
    magiccube (*annealing)(magiccube, double(*)(magiccube), double(*)(double), double);
    double (*temperature)(double);

    switch (obj_option) {
        case 0:
            objective = line_objective_function;
            restart = random_restart_hill_climbing_value;
            annealing = simulated_annealing_value;
            break;
        case 1:
            objective = std_objective_function;
            restart = random_restart_hill_climbing_cost;
            annealing = simulated_annealing_cost;
            break;
        default:
            return 0;
    }
    
    switch (temp_option) {
        case 0:
            temperature = division_temperature_function;
    }

    
    // int numbers[125];
    // int solution[125] = {25,16,80,104,90,115,98,4,1,97,42,111,85,2,75,66,72,27,102,48,67,18,119,106,5,91,77,71,6,70,52,64,117,69,13,30,118,21,123,23,26,39,92,44,114,116,17,14,73,95,47,61,45,76,86,107,43,38,33,94,89,68,63,58,37,32,93,88,83,19,40,50,81,65,79,31,53,112,109,10,12,82,34,87,100,103,3,105,8,96,113,57,9,62,74,56,120,55,49,35,121,108,7,20,59,29,28,122,125,11,51,15,41,124,84,78,54,99,24,60,36,110,46,22,101};
    // int false[125] = {25,16,80,104,90,115,98,4,1,97,42,111,85,2,75,66,72,27,102,48,67,18,119,106,5,91,77,71,6,70,52,64,117,69,13,30,118,21,123,23,26,39,92,44,114,116,17,14,73,95,47,61,45,76,86,107,43,38,33,94,89,68,63,58,37,32,93,88,83,19,40,50,81,65,79,31,53,112,109,10,12,82,34,87,100,103,3,105,9,96,113,57,8,62,74,56,120,55,49,35,121,108,7,20,59,29,28,122,125,11,51,15,41,124,84,78,54,99,24,60,36,110,46,22,101};
    
    // randomise seed
    srand(time(NULL));
    rand();

    // for (int i = 0; i < 125; i++) {
    //     numbers[i] = i+1;
    // }

    // magiccube mySolution;
    // magiccube myCube;
    // magiccube nextCube;
    // magiccube myFalse;
    // magiccube mySolved;

    // mySolution = create_magic_cube(solution);
    // myCube = random_magic_cube();
    // nextCube = random_neighbor(myCube);
    // myFalse = create_magic_cube(false);
    // mySolved = steepest_neighbor_value(myFalse, line_objective_function);

    // display_cube(mySolution);
    // display_cube(myCube);
    // display_cube(nextCube);
    // display_cube(myFalse);
    // display_cube(mySolved);

    // printf("%Lf %Lf %Lf\n", std_objective_function(myFalse), std_objective_function(mySolved), std_objective_function(myCube));
    // printf("%d, %d, %d\n", line_objective_function(mySolution), line_objective_function(myCube), line_objective_function(nextCube));

    magiccube myCube = restart(objective, 10);
    display_cube(myCube);
    return 0;
}