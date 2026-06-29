#include <stdio.h>

int main() {

    char grade = 't';

    switch(grade) {
        case 'A':
        case 'a':
            printf("Greate job! you've got an A!\n");
            break;
        case 'B':
        case 'b':
            printf("Nice ! you've got a B!\n");
            break;
        case 'C':
        case 'c':
            printf("OK! C is nice ! keep improving !\n");
            break;
        case 'D':
        case 'd':
            printf("That's fine, you've got a D!, keep on studying hard and you'll make it!\n");
            break;
        case 'E':
        case 'e':
            printf("That was close.. but you got out of it safely. study better next time !\n");
            break;
        case 'F':
        case 'f':
            printf("F :( you failed..");
            break;
        default:
            printf("INVALID GRADE!\n");
    };

    return 0;
}