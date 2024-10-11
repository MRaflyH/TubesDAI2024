#include "magic_cube.h"

const int magic_const = 315;

magiccube create_magic_cube(int* numbers) {
    magiccube new_cube = (magiccube)malloc(sizeof(int)*125);
    if (new_cube == NULL) {
        printf("Memory allocation failed.\n");
        return NULL;
    }
    for (int i = 0; i < 125; i++) {
        new_cube[i] = numbers[i];
    }
    return new_cube;
}

void free_cube(magiccube magic_cube) {
    // for (int i = 0; i < 125; i++) {
    //     free(magic_cube[i]);
    // }
    free(magic_cube);
}

magiccube deep_copy_magic_cube(magiccube magic_cube) {
    magiccube new_cube = (magiccube)malloc(sizeof(int)*125);
    if (new_cube == NULL) {
        printf("Memory allocation failed.\n");
        return NULL;
    }
    for (int i = 0; i < 125; i++) {
        new_cube[i] = magic_cube[i];
    }
    return new_cube;
}

magiccube random_magic_cube() {
    int numbers[125];
    for (int i = 0; i < 125; i++) {
        numbers[i] = i+1;
    }
    magiccube new_cube = create_magic_cube(numbers);
    int j;
    for (int i = 0; i < 124; i++) {
        j = random_int(124-i) + i + 1;
        cube_swap(new_cube, i, j);
    }
    return new_cube;
}

double line_objective_function(magiccube magic_cube) {
    int point, line_sum_1, line_sum_2, line_sum_3, line_sum_4, line_sum_5, line_sum_6, mirr;
    point = 0;
    // rows, columns, slices
    for (int k = 0; k < 5; k++) {
        for (int j = 0; j < 5; j++) {
            line_sum_1 = 0;
            line_sum_2 = 0;
            line_sum_3 = 0;
            for (int i = 0; i < 5; i++) {
                line_sum_1 += magic_cube[25*k + 5*j + i];
                line_sum_2 += magic_cube[25*k + 5*i + j];
                line_sum_3 += magic_cube[25*j + 5*i + k];
            }
            if (line_sum_1 == magic_const) point++;
            if (line_sum_2 == magic_const) point++;
            if (line_sum_3 == magic_const) point++;
        }
    }
    // face diagonals
    for (int j = 0; j < 5; j++) {
        line_sum_1 = 0;
        line_sum_2 = 0;
        line_sum_3 = 0;
        line_sum_4 = 0;
        line_sum_5 = 0;
        line_sum_6 = 0;
        for (int i = 0; i < 5; i++) {
            mirr = 4-i;
            line_sum_1 += magic_cube[25*j + 5*i + i];
            line_sum_2 += magic_cube[25*j + 5*mirr + mirr];
            line_sum_3 += magic_cube[25*i + 5*j + i];
            line_sum_4 += magic_cube[25*mirr + 5*j + mirr];
            line_sum_5 += magic_cube[25*i + 5*i + j];
            line_sum_6 += magic_cube[25*mirr + 5*mirr + j];
        }
        if (line_sum_1 == magic_const) point++;
        if (line_sum_2 == magic_const) point++;
        if (line_sum_3 == magic_const) point++;
        if (line_sum_4 == magic_const) point++;
        if (line_sum_5 == magic_const) point++;
        if (line_sum_6 == magic_const) point++;
    }
    // space diagonals
    line_sum_1 = 0;
    line_sum_2 = 0;
    line_sum_3 = 0;
    line_sum_4 = 0;
    for (int i = 0; i < 5; i++) {
        mirr = 4-i;
        line_sum_1 += magic_cube[25*i + 5*i + i];
        line_sum_2 += magic_cube[25*i + 5*i + mirr];
        line_sum_3 += magic_cube[25*mirr + 5*i + i];
        line_sum_4 += magic_cube[25*mirr + 5*i + mirr];
    }
    if (line_sum_1 == magic_const) point++;
    if (line_sum_2 == magic_const) point++;
    if (line_sum_3 == magic_const) point++;
    if (line_sum_4 == magic_const) point++;
    return (double) point;
}

double std_objective_function(magiccube magic_cube) {
    int line_sum_1, line_sum_2, line_sum_3, line_sum_4, line_sum_5, line_sum_6, mirr;
    double std;
    std = 0;
    // rows, columns, slices
    for (int k = 0; k < 5; k++) {
        for (int j = 0; j < 5; j++) {
            line_sum_1 = 0;
            line_sum_2 = 0;
            line_sum_3 = 0;
            for (int i = 0; i < 5; i++) {
                line_sum_1 += magic_cube[25*k + 5*j + i];
                line_sum_2 += magic_cube[25*k + 5*i + j];
                line_sum_3 += magic_cube[25*j + 5*i + k];
            }
            std += powl(line_sum_1 - magic_const, 2);
            std += powl(line_sum_2 - magic_const, 2);
            std += powl(line_sum_3 - magic_const, 2);
        }
    }
    // face diagonals
    for (int j = 0; j < 5; j++) {
        line_sum_1 = 0;
        line_sum_2 = 0;
        line_sum_3 = 0;
        line_sum_4 = 0;
        line_sum_5 = 0;
        line_sum_6 = 0;
        for (int i = 0; i < 5; i++) {
            mirr = 4-i;
            line_sum_1 += magic_cube[25*j + 5*i + i];
            line_sum_2 += magic_cube[25*j + 5*mirr + mirr];
            line_sum_3 += magic_cube[25*i + 5*j + i];
            line_sum_4 += magic_cube[25*mirr + 5*j + mirr];
            line_sum_5 += magic_cube[25*i + 5*i + j];
            line_sum_6 += magic_cube[25*mirr + 5*mirr + j];
        }
        std += powl(line_sum_1 - magic_const, 2);
        std += powl(line_sum_2 - magic_const, 2);
        std += powl(line_sum_3 - magic_const, 2);
        std += powl(line_sum_4 - magic_const, 2);
        std += powl(line_sum_5 - magic_const, 2);
        std += powl(line_sum_6 - magic_const, 2);
    }
    // space diagonals
    line_sum_1 = 0;
    line_sum_2 = 0;
    line_sum_3 = 0;
    line_sum_4 = 0;
    for (int i = 0; i < 5; i++) {
        mirr = 4-i;
        line_sum_1 += magic_cube[25*i + 5*i + i];
        line_sum_2 += magic_cube[25*i + 5*i + mirr];
        line_sum_3 += magic_cube[25*mirr + 5*i + i];
        line_sum_4 += magic_cube[25*mirr + 5*i + mirr];
    }
    std += powl(line_sum_1 - magic_const, 2);
    std += powl(line_sum_2 - magic_const, 2);
    std += powl(line_sum_3 - magic_const, 2);
    std += powl(line_sum_4 - magic_const, 2);
    std = sqrtl(std/125);
    return std;
}

magiccube steepest_neighbor_value(magiccube magic_cube, double (*objective_function)(magiccube)) {
    int cube_index_1, cube_index_2, steepest_value, temp_value;
    magiccube new_cube;
    cube_index_1 = 0;
    cube_index_2 = 1;
    cube_swap(magic_cube, cube_index_1, cube_index_2);
    steepest_value = objective_function(magic_cube);
    cube_swap(magic_cube, cube_index_1, cube_index_2);
    for (int i = 0; i < 124; i++) {
        for (int j = i+1; j < 125; j++) {
            cube_swap(magic_cube, i, j);
            temp_value = objective_function(magic_cube);
            if (temp_value > steepest_value) {
                steepest_value = temp_value;
                cube_index_1 = i;
                cube_index_2 = j;
            }
            cube_swap(magic_cube, i, j);
        }
    }
    cube_swap(magic_cube, cube_index_1, cube_index_2);
    new_cube = deep_copy_magic_cube(magic_cube);
    cube_swap(magic_cube, cube_index_1, cube_index_2);
    return new_cube;
}

magiccube steepest_neighbor_cost(magiccube magic_cube, double (*objective_function)(magiccube)) {
    int cube_index_1, cube_index_2, steepest_value, temp_value;
    magiccube new_cube;
    cube_index_1 = 0;
    cube_index_2 = 1;
    cube_swap(magic_cube, cube_index_1, cube_index_2);
    steepest_value = objective_function(magic_cube);
    cube_swap(magic_cube, cube_index_1, cube_index_2);
    for (int i = 0; i < 124; i++) {
        for (int j = i+1; j < 125; j++) {
            cube_swap(magic_cube, i, j);
            temp_value = objective_function(magic_cube);
            if (temp_value < steepest_value) {
                steepest_value = temp_value;
                cube_index_1 = i;
                cube_index_2 = j;
            }
            cube_swap(magic_cube, i, j);
        }
    }
    cube_swap(magic_cube, cube_index_1, cube_index_2);
    new_cube = deep_copy_magic_cube(magic_cube);
    cube_swap(magic_cube, cube_index_1, cube_index_2);
    return new_cube;
}

magiccube random_neighbor(magiccube magic_cube) {
    magiccube new_cube = deep_copy_magic_cube(magic_cube);
    int cube_index_1, cube_index_2;
    cube_index_1 = random_int(125);
    cube_index_2 = random_int(125);
    while (cube_index_1 == cube_index_2) {
        cube_index_1 = random_int(125);
        cube_index_2 = random_int(125);
    }
    cube_swap(new_cube, cube_index_1, cube_index_2);
    return new_cube;
}

void cube_swap(magiccube magic_cube, int cube_index_1, int cube_index_2) {
    magic_cube[cube_index_1] = magic_cube[cube_index_1] ^ magic_cube[cube_index_2];
    magic_cube[cube_index_2] = magic_cube[cube_index_1] ^ magic_cube[cube_index_2];
    magic_cube[cube_index_1] = magic_cube[cube_index_1] ^ magic_cube[cube_index_2];
}

void display_cube(magiccube magic_cube) {
    for (int i = 0; i < 125; i++) {
        printf("%d ",magic_cube[i]);
    }
    printf("\n");
}

int random_int(int max_number) {
    // clock_t time = clock();
    // return time % max_number;
    return rand() % max_number;
}
