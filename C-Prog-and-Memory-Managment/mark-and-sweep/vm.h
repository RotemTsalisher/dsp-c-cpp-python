#ifndef __VM__H
#define __VM__H

#include <stdio.h>
#include <stdlib.h>
#include "myStack.h"

struct VirtualMachine {
   stack_t *frames;
   stack_t *objects;
};
struct StackFrame {
   stack_t *references;
};
typedef struct VirtualMachine vm_t;
typedef struct StackFrame     frame_t;

vm_t *vm_new();
void vm_free(vm_t* vm);

void vm_frame_push(vm_t *vm, frame_t* frame);
frame_t* vm_new_frame(vm_t *vm);
void frame_free(frame_t *frame);
#endif