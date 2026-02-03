#include <stdio.h>

// Task 1: not using not, and, or etc.
void checkX(int x)
{
    if (x <= -30) { 
        printf("%d", ((3*x*x*x)/4) - 5);
        return;
    }
    if (x > -15) {
        if (x <= 3) {
            printf("%d", (4*x*x) + 2);
            return;
        }
    }
    if (x > 20) {
        printf("%d", ((3*x*x*x)/4) - 5);
        return;
    }

    printf("%s", "The function is not defined.");
}

int main()
{
    /*
        Variant - 14

        4x2 + 2 => (-15, 3]
        3x3/4 - 5 => (-inf, -30] U (20, +inf)
    */

    int testArr[] = { -45, -30, -25, -15, -10, 3, 4, 20, 40, 100 };

    int i;

    printf("%s\n", "Running tests:");
    for (i = 0; i < (sizeof(testArr) / sizeof(testArr[0])); i++) {
        printf("Input data: x=%d\n", testArr[i]);
        printf("Result: ");
        checkX(testArr[i]);

        printf("\n");
    }

    return 0;
}

