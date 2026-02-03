# include <stdio.h>
# include <math.h>
#include <stdbool.h>
// For sleep()
#include <unistd.h>

// Ordered matrix traversal

int main() {
	// Note that rows amount must be even to display all the matrix elements according to task variant
    int rows = 24;
    int cols = 80;

    // Create matrix
    char matrix[rows][cols];
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            matrix[i][j] = '.';
        };
    };

	// Start position according to variant №14

	// Getting bottom-central row index
	int i = rows / 2;
	int normalization = (rows - 1) - i;
	int j = abs(normalization - (cols - 1));

	while (true) {
		// While loop iteration: left -> up -> right -> down

		// Left
		for (j; j >= normalization; j--) {
			usleep(1000);
			printf("\033[%d;%dH%c", i+1, j+1, matrix[i][j]);
		};

		j++;

		// Up
		for (i; i >= normalization; i--) {
			usleep(1000);
			printf("\033[%d;%dH%c", i+1, j+1, matrix[i][j]);
		};

		i++;

		normalization -= 1;

		// Right
		for (j; j <= (cols - 1) - normalization; j++) {
			usleep(1000);

			if (j == (cols - 1) - normalization && normalization == -1) {
				return 0;
			};

			printf("\033[%d;%dH%c", i+1, j+1, matrix[i][j]);
		};

		if (normalization == -1) {
    		return 0;
		};

		j--;

		// Down
		for (i; i <= (rows - 1) - normalization; i++) {
			usleep(1000);
			printf("\033[%d;%dH%c", i+1, j+1, matrix[i][j]);
		};

		i--;

	};

    return 0;
};