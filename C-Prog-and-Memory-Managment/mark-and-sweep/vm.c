#include <stdio.h>
#include <stdlib.h>
#include "vm.h"

vm_t* vm_new() {
    
    vm_t* new = (vm_t*)malloc(sizeof(vm_t));
    if(!(new)) return NULL;

    new->frames = stack_new(8);
    if(!(new->frames)) {
        free(new);
        return NULL;
    };

    new->objects = stack_new(8);
    if(!(new->objects)) {
        free(new);
        return NULL;
    };

    return new;
};

void vm_free(vm_t* vm) {
    if(!(vm)) return ;

    if(vm->frames)  stack_free(vm->frames);
    if(vm->objects) stack_free(vm->objects);

    free(vm);
}

frame_t* vm_new_frame(vm_t *vm) {
    frame_t *frame = malloc(sizeof(frame_t));
    if(!(frame)) return NULL;

    frame->references = stack_new(8);
    if(!(frame->references)) {
        free(frame);
        return NULL;
    };

    vm_frame_push(vm, frame);

    return frame;
}

void frame_free(frame_t *frame) {

    if(!(frame)) return ;

    stack_free(frame->references);
    free(frame);

}

void vm_frame_push(vm_t *vm, frame_t *frame) {
    if(!(vm) || !(frame)) return ;

    stack_push(vm->frames, (void*)frame);
};
