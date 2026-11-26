#include "data-node-lib.h"

node_t* new_node_int(int val) {

    node_t* new = (node_t*)malloc(sizeof(node_t));
    
    if(!(new)) return NULL;
    new->type = INT;
    new->data.int_v = val;
    new->refcount = 1;

    return new;
};

node_t* new_node_float(float val) {
    
    node_t* new = (node_t*)malloc(sizeof(node_t));
    
    if(!(new)) return NULL;
    new->type = FLOAT;
    new->data.float_v = val;
    new->refcount = 1;

    return new;
};

bool_t  free_node(node_t* node) {
    
    if(!(node)) return 1;

    free(node);
    node = NULL;
    return 0;
}

bool_t  set_node_data(node_t* node, void* data) {
    
    if(!(node) || !(data)) return 1;
    
    switch(node->type) {
        case INT:
            node->data.int_v = *(int*)data;
            break;
        case FLOAT:
            node->data.float_v = *(float*)data;
            break;
        default:
            return 1;
    }

    return 0;
};

bool_t  get_node_data(node_t* node, void* data) {
    
    int* tmp_int;
    float* tmp_float;

    if(!(node) || !(data)) return 1;
    switch (node->type) {
        case INT:
            tmp_int = (int*)data;
            *tmp_int = node->data.int_v;
            break;
        case FLOAT:
            tmp_float = (float*)data;
            *tmp_float = node->data.float_v;
            break;
        default:
            return 1; 
    };
    return 0;
}


node_t* ref_to(node_t* node) {
    
    if(!(node)) return NULL;

    node_t* new_ref = node;
    node->refcount++;

    return new_ref;
};

void deref_node(node_t* deref) {

    if(!(deref) || deref->refcount == 0) return;

    deref->refcount--;
    
    if(deref->refcount == 0){    
        free_node(deref);
        return;
    };

    deref = NULL;
}
node_refcount_t get_node_refcount(node_t* node) {
    if(!(node)) return 0;

    return node->refcount;
};