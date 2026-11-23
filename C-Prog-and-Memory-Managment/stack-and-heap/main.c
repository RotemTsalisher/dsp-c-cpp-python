#include <stdio.h>

static void* ptr_foo = NULL;
static void* ptr_bar = NULL;

void foo(int a, int tmp);
void bar(int v);

int main() {

    foo(1, 100);

    printf("Diff in bytes between foo and bar stack: %ld\n", (char*)ptr_foo - (char*)ptr_bar);
    return 0;
};


void foo(int a, int tmp) {

    // first stored what is passed
    // second stored what is allocated
    int b = 32;
    char arr_[28] = {'a', 'b', 'c', 'd'};

    ptr_foo = (void*)&a;
    printf("Address of foo stack: %p\n", (void*)ptr_foo);
    bar(2);
};

void bar(int v) {
    int c = 64;
    char arr_[4] = {'e', 'f', 'g', 'h'};

    ptr_bar = (void*)&v;
    printf("Address of bar stack: %p\n", (void*)ptr_bar);
};