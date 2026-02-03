#include <stdio.h>
#include <stdbool.h>

// Matrix first row and last col most left element binary search implementation

void createMatrix(bool ascending, int instances, int rows, int cols, int matrix[rows][cols]) {
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

int main() {
    printf("%s", "Enter the matrix rows amount: ");
    int rows;
    scanf("%d",&rows);

    printf("%s", "Enter the matrix cols amount: ");
    int cols;
    scanf("%d",&cols);

    printf("%s", "Enter target matrix element: ");
    int target;
    scanf("%d",&target);

    int matrix[rows][cols];

	bool ascending = true; // Set to true to create matrix with ascending matrix
	int instances = 1; // Set amount of each element instances. For example instances=2 -> 0, 0, 1, 1, 2, 2
	createMatrix(ascending, instances, rows, cols, matrix);

    // Display matrix
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            printf("%3d ", matrix[i][j]);
        }
        printf("\n");
    }

    // Find target in first row
	int low = 0;
	int high = cols - 1;
	int mid;

	int result = -1;

	while (low <= high) {
		mid = (high + low) / 2;

		if (matrix[0][mid] < target) {
			if (ascending) {
				low = mid + 1;
			} else {
				high = mid - 1;
			}
		} else if (matrix[0][mid] > target) {
			if (ascending) {
				high = mid - 1;
			} else {
				low = mid + 1;
			}
		} else {
			result = mid;
			high = mid - 1;

		}
	}

	if (!(result == -1)) {
		printf("%s\n", "Target Number Found in First Row!");
		printf("Coordinates: %d %d", 0, result);
		return 0;
	}

	low = 0;
	high = rows - 1;
	result = -1;

	while (low <= high) {
		mid = (high + low) / 2;

		if (matrix[mid][cols-1] < target) {
			if (ascending) {
				low = mid + 1;
			} else {
				high = mid - 1;
			}
		} else if (matrix[mid][cols-1] > target) {
			if (ascending) {
				high = mid - 1;
			} else {
				low = mid + 1;
			}
		} else {
			result = mid;
			high = mid - 1;
		}
	}

	if (!(result == -1)) {
		printf("%s\n", "Target Number Found in Last Column!");
		printf("Coordinates: %d %d", result, cols - 1);
		return 0;
	}

	printf("%s", "Target Number Not Found!");
    return 0;
}