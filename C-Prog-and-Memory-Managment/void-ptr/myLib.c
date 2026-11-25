#include ".\myLib.h"


void print_value(void *data, snek_obj_kind_t type) {

    switch(type) {
        case INT:
            snek_int_t* obj_int = (snek_int_t*)data;
            printf("int value: %d\n", obj_int->val);
            break;
        case FLOAT:
            snek_float_t* obj_float = (snek_float_t*)data;
            printf("float value: %5.3f\n", obj_float->val);
            break;
        
        case BOOL:
            snek_bool_t* obj_bool = (snek_bool_t*)data;
            printf("bool value: %u\n", obj_bool->val);
            break;

        default:
            printf("default print!\n");
            break;
    }
}

void init_value(void *data, snek_obj_kind_t type) {

    switch(type) {
        case INT:
            snek_int_t* obj_int = (snek_int_t*)data;
            obj_int->val = 0;
            break;
        case FLOAT:
            snek_float_t* obj_float = (snek_float_t*)data;
            obj_float->val = 0.0f;
            break;
        
        case BOOL:
            snek_bool_t* obj_bool = (snek_bool_t*)data;
            obj_bool->val = 0U;
            break;

        default:
            printf("default init!\n");
            break;
    }
}

void set_value(void *data, snek_obj_kind_t type, const void* val) {
    
    switch(type) {
        case INT:
            snek_int_t* obj_int = (snek_int_t*)data;
            obj_int->val = *((int*)val);
            break;
        case FLOAT:
            snek_float_t* obj_float = (snek_float_t*)data;
            obj_float->val = *((float*)val);
            break;
        
        case BOOL:
            snek_bool_t* obj_bool = (snek_bool_t*)data;
            obj_bool->val = *((unsigned int*)val);
            break;

        default:
            printf("default set value!\n");
            break;
    }
}

void get_value(void *data, snek_obj_kind_t type, void* val) {
    
    switch(type) {
        case INT:
            snek_int_t* obj_int = (snek_int_t*)data;
            int* val_int = (int*)val;
            *val_int = obj_int->val;
            break;
        case FLOAT:
            snek_float_t* obj_float = (snek_float_t*)data;
            float* val_float = (float*)val;
            *val_float = obj_float->val;
            break;
        
        case BOOL:
            snek_bool_t* obj_bool = (snek_bool_t*)data;
            unsigned int* val_bool = (unsigned int*)val;
            *val_bool = obj_bool->val;
            break;

        default:
            printf("default set value!\n");
            break;
    }
}

void swap_structs(void* a, void* b, int size) {
    void* tmp = malloc(size);
    
    memcpy(tmp, a, size);
    memcpy(a, b, size);
    memcpy(b, tmp, size);
}

void swap_strings(char** str1, char** str2) {
    char* tmp = *str1;
    *str1 = *str2;
    *str2 = tmp;
}


