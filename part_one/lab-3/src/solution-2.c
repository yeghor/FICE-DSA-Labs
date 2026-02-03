#include <stdio.h>
#include <stdbool.h>

#include <unistd.h>

#define ROW 23
#define COL 80

void newMatrix(char matrix[ROW][COL]) {
    int fill_count = 1;

    for (int j = 0; j < COL; j++) {
        if (j % 2 == 0) {
            for (int i = 0; i < ROW; i++) {
                matrix[i][j] = '#';
            }
        } else {
            for (int i = ROW - 1; i >= 0; i--) {
                matrix[i][j] = '#';
            }
        }
    }
}

typedef struct {
    int x;
    int y;
} Point;

void Pmatrix(char matrix[ROW][COL]) {

    int startX = (COL - 1) / 2;

    Point p1;
    Point p2;

    p1.y = startX;
    p1.x = ROW - 1;;

    p2.y = startX + 1;
    p2.x = 0;

    while (p1.y >= 0 && p2.y < COL) {

        while (p2.x < ROW && p1.x >= 0) {
            usleep(10000);
            printf("\033[%d;%dH%c", p1.x+1, p1.y+1, matrix[p1.x][p1.y]);
            printf("\033[%d;%dH%c", p2.x+1, p2.y+1, matrix[p2.x][p2.y]);

            p1.x--;
            p2.x++;
        }
        p1.x += 1;
        p2.x -= 1;

        p1.y--;
        p2.y++;

        while (p1.x < ROW && p2.x >= 0) {
            usleep(10000);
            printf("\033[%d;%dH%c", p1.x+1, p1.y+1, matrix[p1.x][p1.y]);
            printf("\033[%d;%dH%c", p2.x+1, p2.y+1, matrix[p2.x][p2.y]);

            p1.x++;
            p2.x--;
        }
        p1.x -= 1;
        p2.x += 1;

        p1.y--;
        p2.y++;
    }
}

int main() {
    char matrix[ROW][COL];
    newMatrix(matrix);
    printf("Matrix (%dx%d).\n", ROW, COL);
    Pmatrix(matrix);
    return 0;
}