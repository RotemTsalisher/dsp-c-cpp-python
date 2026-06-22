#include <stdio.h>
#define STRING_WITH_WHITESPACE

int main() {
    
#ifdef INTEGER
    int user_age = 0;
    printf("Enter you age: ");
    scanf("%d", &user_age);

    printf("Echo user age: %d\n", user_age);
#elifdef DOUBLE 
    double gpa = 0.0;
    printf("Enter you gpa : ");
    scanf("%lf", &gpa);
    printf("Echo user gpa : %.2lf", gpa);

#elifdef STRING
    
    char name[20];
    printf("Enter you name : ");
    scanf("%s", name);
    printf("Echo user name : %s", name);

#elifdef STRING_WITH_WHITESPACE
    char name[40];
    printf("Enter full name : ");
    fgets(name, 20, stdin);
    printf("Echo user full name : %s", name);
#endif
    return 0;
}