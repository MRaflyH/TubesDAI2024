#ifndef ARRAY_H
#define ARRAY_H

#include <stdio.h>
#include <stdlib.h>
#include "magic_cube.h"

int* create_array(int length);
void clear_array(int* list);
int array_size(int list[]);
int find_array_index(int list[], int element);
int max_array(int list[], int element);
void append_array_element(int* list, int element);
void append_array_array(int* list, int* elements);

magiccube* create_population(int length);
magiccube* deep_copy_population(magiccube magic_cube);
void clear_population(magiccube* list);
int population_size(magiccube list[]);
int population_find_index(magiccube list[], magiccube element);
void append_population_element(magiccube* list, magiccube element);
void append_population_population(magiccube* list, magiccube* elements);

int* random_array(int start_range, int end_range, int amount);
int* weighted_random_array(int start_range, int end_range, int amount, int weight[]);

#endif