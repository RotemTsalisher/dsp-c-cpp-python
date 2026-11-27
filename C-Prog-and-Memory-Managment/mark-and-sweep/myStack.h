#ifndef __MY__STACK__H
#define __MY__STACK__H

#include <stdio.h>
#include <stdlib.h>

struct stack {
    
    int count;
    int capacity;
    void **data;
};

typedef struct stack stack_t;

stack_t* stack_new(int capacity_);
void stack_push(stack_t *stack, void* obj);
void* stack_pop(stack_t *stack);
void stack_free(stack_t *stack);

#endif