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

int main(void)
{
    stack_t *stack = stack_new(2);

    if (stack == NULL) {
        printf("Failed to create stack\n");
        return 1;
    }

    int a = 10;
    int b = 20;
    int c = 30;
    int d = 40;

    printf("Initial:\n");
    printf("count = %d\n", stack->count);
    printf("capacity = %d\n\n", stack->capacity);

    /* PUSH TEST */
    stack_push(stack, &a);
    stack_push(stack, &b);
    stack_push(stack, &c);  /* triggers realloc */
    stack_push(stack, &d);

    printf("After push:\n");
    printf("count = %d\n", stack->count);
    printf("capacity = %d\n\n", stack->capacity);

    for (int i = 0; i < stack->count; ++i) {
        printf("stack[%d] = %d\n",
               i,
               *(int*)stack->data[i]);
    }

    /* POP TEST */
    printf("\n--- POP TEST ---\n");

    int *popped = (int*)stack_pop(stack);

    if (popped != NULL) {
        printf("popped = %d\n", *popped);
    }

    popped = (int*)stack_pop(stack);

    if (popped != NULL) {
        printf("popped = %d\n", *popped);
    }

    printf("\nAfter pop:\n");
    printf("count = %d\n", stack->count);
    printf("capacity = %d\n\n", stack->capacity);

    printf("Remaining stack:\n");

    for (int i = 0; i < stack->count; ++i) {
        printf("stack[%d] = %d\n",
               i,
               *(int*)stack->data[i]);
    }

    /* FREE TEST */
    printf("\nFreeing stack...\n");

    stack_free(stack);

    printf("Stack freed.\n");

    return 0;
}

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