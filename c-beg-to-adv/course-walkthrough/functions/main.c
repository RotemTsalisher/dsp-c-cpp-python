#include <stdio.h>

void say_hi();
void print_messege(const char* messege);
void print_name_and_age(const char* name, int age);

int main() {

    say_hi();
    print_messege("Hi!, my name is Rotem");
    print_name_and_age("Rotem", 34);
    return 0;
};

void say_hi() {
    printf("Hi user!\n");

    return ;
}

void print_messege(const char* messege) {
    printf("%s\n", messege);
    return ;
}

void print_name_and_age(const char* name, int age) {
    printf("Hello! my name is %s, and I am %d years old\n", name, age);
    return ;
}