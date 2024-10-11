#ifndef MAGIC_CUBE_H
#define MAGIC_CUBE_H

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

typedef int* magiccube;
extern const int magic_const;

magiccube create_magic_cube(int* numbers);
void free_cube(magiccube magic_cube);
magiccube deep_copy_magic_cube(magiccube magic_cube);
magiccube random_magic_cube();
double line_objective_function(magiccube magic_cube);
double std_objective_function(magiccube magic_cube);
magiccube steepest_neighbor_value(magiccube magic_cube, double (*objective_function)(magiccube));
magiccube steepest_neighbor_cost(magiccube magic_cube, double (*objective_function)(magiccube));
magiccube random_neighbor(magiccube magic_cube);
void cube_swap(magiccube magic_cube, int swap_index_1, int swap_index_2);
void display_cube(magiccube magic_cube);
int random_int(int max_number);

#endif