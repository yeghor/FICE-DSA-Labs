# include <stdio.h>
# include <math.h>

// Program that uses nested cycles to calculate the expression

double calculate(int n) {
    double result = 1.0;
    int operations = 0;

    for(int i = 1; i <= n; i++) {

		double numerator;

        numerator = cos(i) + 1;
        operations += 2;

		double denominator = 0;

        for(int j = 1; j <= i; j++) {
            operations += 2;
            denominator += sin(j);

            operations += 1; // Loop increment
        }

        result *= (numerator / denominator);
        operations += 2;

        operations += 1; // Loop increment
    }

    printf("Operations: %d\n ", operations);

    return result;
}

int main() {
    int n;
    printf("Enter the n number: ");
    scanf("%d", &n);

    double result = calculate(n);

    printf("Result: %.7f\n", result);

    return 0;
}
