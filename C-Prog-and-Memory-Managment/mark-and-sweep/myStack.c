#include "./myStack.h"

stack_t* stack_new(int capacity_) {

    stack_t *new = (stack_t*)malloc(sizeof(stack_t));

    if(!(new)) {
        return NULL;
    };

    new->count = 0;
    new->capacity = capacity_;

    new->data = (void**)malloc(sizeof(void*) * new->capacity);
    if(!(new->data)) {
        return NULL;
    }; 
    
    return new;
}

void stack_push(stack_t *stack, void* obj) {

    if(stack->capacity == stack->count) {
        stack->capacity *= 2;
        stack->data = (void**)realloc(stack->data, sizeof(void*) * stack->capacity);
    };

    stack->data[stack->count++] = obj;
};

void* stack_pop(stack_t *stack) {
    if(stack->count == 0) {
        return NULL;
    };

    stack->count--;
    return stack->data[stack->count];
}

void stack_free(stack_t *stack) {
    if(stack == NULL) {
        return;
    };

    if(stack->data) {
        free(stack->data);
    };

    free(stack);
};