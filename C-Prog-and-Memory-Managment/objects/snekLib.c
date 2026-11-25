#include "snekLib.h"
#include <stdlib.h>
#include <string.h>

snek_object_t* new_snek_int(const int value) {
    
    snek_object_t* new = (snek_object_t*)malloc(sizeof(snek_object_t));
    
    if(!(new)) {
        return NULL;
    };
    new->type = INT;
    new->data.int_v = value;

    return new;
}

snek_object_t* new_snek_float(const float value) {

    snek_object_t* new = (snek_object_t*)malloc(sizeof(snek_object_t));

    if(!(new)) {
        return NULL;
    };
    new->type = FLOAT;
    new->data.float_v = value;

    return new;
};

snek_object_t* new_snek_string(const char* value) {

    snek_object_t* new = (snek_object_t*)malloc(sizeof(snek_object_t));

    if(!(new)) {
        return NULL;
    };
    new->type = STR;
    new->data.string_v = (char*)malloc(sizeof(char) * (strlen(value) + 1));

    if(!(new->data.string_v)) {
        free(new);
        return NULL;
    };

    strcpy(new->data.string_v, value);

    return new;
};

snek_object_t* new_snek_vector(snek_object_t* x_, snek_object_t* y_, snek_object_t* z_) {

    snek_object_t* new = (snek_object_t*)malloc(sizeof(snek_object_t));
    
    if(!(new)) {
        return NULL;
    };

    new->type = VECTOR;
    new->data.vector_v = (snek_vector_t){.x = x_ , .y = y_, .z = z_};

    return new;
};

snek_object_t* new_snek_array(int size) {

    snek_object_t* new = (snek_object_t*)malloc(sizeof(snek_object_t));

    if(!(new)) {
        return NULL;
    };

    new->type = ARRAY;
    new->data.array_v.size = size;
    new->data.array_v.arr = (snek_object_t**)malloc(sizeof(snek_object_t*)*size);

    if(!(new->data.array_v.arr)) {
        free(new);
        return NULL;
    };

    for(int i = 0; i < size; ++i) {
        new->data.array_v.arr[i] = NULL;
    };

    return new;
};

int snek_array_set(snek_object_t* obj, int index, snek_object_t* value) {
    
    if( (!(obj) | (!value)) ) {
        return -1;
    };

    if(obj->type != ARRAY) {
        return -1;
    };

    if(!(index < obj->data.array_v.size)) {
        return -1;
    };

    obj->data.array_v.arr[index] = value;
    return 0;
};

snek_object_t* snek_array_get(snek_object_t* obj, int index) {
    
    if( (!(obj)) | (obj->type != ARRAY) | (!(index < obj->data.array_v.size)) ) {
        return NULL;
    };

    return obj->data.array_v.arr[index];
};

int snek_length(snek_object_t* obj) {

    if(!(obj)) {
        return -1;
    };

    switch(obj->type) {
        case INT:    return 1;
        case FLOAT:  return 1;
        case STR:    return strlen(obj->data.string_v);
        case VECTOR: return 3;
        case ARRAY:  return obj->data.array_v.size;
        default:     return -1;
    };
};