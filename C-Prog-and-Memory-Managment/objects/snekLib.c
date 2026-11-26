#include "snekLib.h"

snek_object_t* new_snek_int(const int value) {
    
    snek_object_t* new = (snek_object_t*)malloc(sizeof(snek_object_t));
    
    if(!(new)) {
        return NULL;
    };

    new->refcount = 1;
    new->type = INT;
    new->data.int_v = value;

    return new;
}

snek_object_t* new_snek_float(const float value) {

    snek_object_t* new = (snek_object_t*)malloc(sizeof(snek_object_t));

    if(!(new)) {
        return NULL;
    };

    new->refcount = 1;
    new->type = FLOAT;
    new->data.float_v = value;

    return new;
};

snek_object_t* new_snek_string(const char* value) {

    if(!(value)) return NULL;

    snek_object_t* new = (snek_object_t*)malloc(sizeof(snek_object_t));

    if(!(new)) {
        return NULL;
    };

    new->refcount = 1;
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

    new->refcount = 1;
    new->type = VECTOR;
    new->data.vector_v = (snek_vector_t){.x = x_ , .y = y_, .z = z_};
    
    refcount_inc(new->data.vector_v.x);
    refcount_inc(new->data.vector_v.y);
    refcount_inc(new->data.vector_v.z);

    return new;
};

snek_object_t* new_snek_array(int size) {

    if(size < 0) return NULL;

    snek_object_t* new = (snek_object_t*)malloc(sizeof(snek_object_t));

    if(!(new)) {
        return NULL;
    };

    new->refcount = 1;
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

    if(!(index < obj->data.array_v.size) || index < 0) {
        return -1;
    };

    obj->data.array_v.arr[index] = value;
    refcount_inc(value);
    if(obj->data.array_v.arr[index]) refcount_dec(obj->data.array_v.arr[index]);

    return 0;
};

snek_object_t* snek_array_get(const snek_object_t* obj, int index) {
    
    if( (!(obj)) || (obj->type != ARRAY) || (!(index < obj->data.array_v.size)) || (!(obj->data.array_v.arr)) || (index < 0) ) {
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
        case STR:    
            if(!(obj->data.string_v)) return -1;
            return strlen(obj->data.string_v);
        case VECTOR: 
            if(!(obj->data.vector_v.x) || !(obj->data.vector_v.y) || !(obj->data.vector_v.z)) return -1;
            return 3;
        case ARRAY:  
            if(!(obj->data.array_v.arr)) return -1;
            return obj->data.array_v.size;
        default:     return -1;
    };
};

snek_object_t* snek_add(const snek_object_t* a, const snek_object_t* b) {
    
    if(!(a) || !(b)) {
        return NULL;
    };

    switch(a->type) {

        case INT:
            switch(b->type) {
                case INT:    return add_snek_int(a, b);
                case FLOAT:  return new_snek_float((float)a->data.int_v + b->data.float_v);
                default: return NULL;
            };
        case FLOAT:
            switch(b->type) {
                case INT:    return new_snek_float(a->data.float_v + (float)b->data.int_v);
                case FLOAT:  return add_snek_float(a, b);
                default: return NULL;
            };
        case STR:
            if(b->type != STR) return NULL;
            return add_snek_string(a, b);
        case VECTOR:
            if(b->type != VECTOR) return NULL;
            return add_snek_vector(a, b);
        case ARRAY:
            if(b->type != ARRAY) return NULL;
            return add_snek_array(a, b);
    };

    return NULL;
}

void refcount_inc(snek_object_t* obj) {

    if(!(obj)) return ;

    obj->refcount++;
    return ;
};

void snek_object_free(snek_object_t* obj) {
    
    if(!(obj)) return ;
    switch(obj->type) {
        case INT: break;
        case FLOAT: break;
        case STR:
            if(obj->data.string_v) free(obj->data.string_v);
            break;

        case VECTOR:
            refcount_dec(obj->data.vector_v.x);
            refcount_dec(obj->data.vector_v.y);
            refcount_dec(obj->data.vector_v.z);
            break;

        case ARRAY:
            for(int i = 0; i < obj->data.array_v.size; ++i) {
                refcount_dec(obj->data.array_v.arr[i]);
            };
            free(obj->data.array_v.arr);
            break;

        default: 
            break;
    };

    free(obj);
    return;
};

void refcount_dec(snek_object_t* obj) {
    if(!(obj)) return ;

    obj->refcount--;
    if(obj->refcount == 0) snek_object_free(obj);
}