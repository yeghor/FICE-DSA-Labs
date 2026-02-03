#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <time.h>

#define ROWS 10
#define COLS 10

void createMatrix(bool ascending, int instances, bool random, int rows, int cols, int matrix[ROWS][COLS]) {
    int value;
    if (!ascending) {
        value = rows * cols;
    } else {
        value = 0;
    }

    if (instances < 1) {
        instances = 1;
    }

    int instancesCounter = 0;

    // Create matrix
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            if (random) {
                matrix[i][j] = rand() % (COLS*ROWS + 1);
                continue;
            }

            matrix[i][j] = value;

            instancesCounter++;

            if (instancesCounter >= instances || instances == 1) {
                instancesCounter = 0;
                if (!ascending) {
                    value -= 1;
                } else {
                    value++;
                }
            }
        }
    }
}

void displayMatrix(int matrix[ROWS][COLS]) {
    for (int i = 0; i < ROWS; i++) {
        for (int j = 0; j < COLS; j++) {
            printf("%3d ", matrix[i][j]);
        }
        printf("\n");
    }
}

int main() {
	srand(time(NULL));

    int matrix[ROWS][COLS];

    createMatrix(false, 1, false, ROWS, COLS, matrix);

    displayMatrix(matrix);

    int i, j;
    int secondIterations = COLS-1;
    int firstIterations = COLS-1;

    for (int iterations = 0; iterations < abs(COLS/2); iterations++ ) {

        i = 0;
        j = 0;

        for (int _ = 0; _ < firstIterations; _++) {
            if (matrix[i][j] < matrix[i+1][j+1]) {
                int temp = matrix[i][j];

                matrix[i][j] = matrix[i+1][j+1];
                matrix[i+1][j+1] = temp;
            }
            i++;
            j++;
        }

        firstIterations -= 1;

        i = ROWS-1;
        j = COLS-1;

        for (int _ = 0; _ < secondIterations; _++) {
            if (matrix[i][j] > matrix[i-1][j-1]) {
                int temp = matrix[i][j];

                matrix[i][j] = matrix[i-1][j-1];
                matrix[i-1][j-1] = temp;
            }
            i -= 1;
            j -= 1;
        }

        secondIterations -= 1;
    }

    printf("\n\n");
    displayMatrix(matrix);
}
