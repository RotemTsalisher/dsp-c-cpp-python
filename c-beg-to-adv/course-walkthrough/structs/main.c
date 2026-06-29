#include <stdio.h>
#include <stdlib.h>

#define MAX_NAME_LEN  50
#define MAX_MAJOR_LEN MAX_NAME_LEN

struct student {

    char name[MAX_NAME_LEN];
    char major[MAX_MAJOR_LEN];
    int age;
    double gpa;
};

typedef struct student Student;

void init_student(Student* s);
void print_student(const Student* s);

int main() {

    Student s;
    init_student(&s);
    print_student(&s);
    return 0;
};

void init_student(Student* s) {
    printf("Enter student name : ");
    fgets(s->name, MAX_NAME_LEN, stdin);

    printf("Enter major : ");
    fgets(s->major, MAX_MAJOR_LEN, stdin);

    printf("Enter student age : ");
    scanf("%d", &(s->age));

    printf("Enter student gpa : ");
    scanf("%lf", &(s->gpa));
    
    return ;
};

void print_student(const Student* s) {
    printf("========== PRINTING STUDENT ==========\n");
    printf("Name  : %s", s->name);
    printf("Major : %s", s->major);
    printf("Age   : %d\n", s->age);
    printf("GPA   : %2.1lf\n", s->gpa);

    return;
};