#include <stdio.h>
#include <stdlib.h>

//#define TYPE_ALLOC(type, ptr) ((type*)malloc(sizeof(type) * (ptr)))
#define TYPE_ALLOC(type, size) (malloc(sizeof(type) * (size)))

enum alloc_type {
    ALLOC_INT,
    ALLOC_CHAR,
    ALLOC_FLOAT,
    ALLOC_DOUBLE
};

typedef enum alloc_type alloc_type_t;

int dynamic_alloc(void** ptr, int size, alloc_type_t type);

int main() {
    int size = 4;
    int* int_ptr = NULL;
    char* char_ptr = NULL;
    float* float_ptr = NULL;
    double* double_ptr = NULL;

    if(dynamic_alloc((void**)&int_ptr, size, ALLOC_INT) == 0) {
        for(int i = 0; i < size; i++) {
            int_ptr[i] = i * 10;
        }
        for(int i = 0; i < size; i++) {
            printf("int_ptr[%d] = %d\n", i, int_ptr[i]);
        }
    }

    if(dynamic_alloc((void**)&char_ptr, size, ALLOC_CHAR) == 0) {
        for(int i = 0; i < size; i++) {
            char_ptr[i] = 'A' + i;
        }
        for(int i = 0; i < size; i++) {
            printf("char_ptr[%d] = %c\n", i, char_ptr[i]);
        }
    }

    if(dynamic_alloc((void**)&float_ptr, size, ALLOC_FLOAT) == 0) {
        for(int i = 0; i < size; i++) {
            float_ptr[i] = (float)i * 1.5f;
        }
        for(int i = 0; i < size; i++) {
            printf("float_ptr[%d] = %.2f\n", i, float_ptr[i]);
        }
    }

    if(dynamic_alloc((void**)&double_ptr, size, ALLOC_DOUBLE) == 0) {
        for(int i = 0; i < size; i++) {
            double_ptr[i] = (double)i * 2.5;
        }
        for(int i = 0; i < size; i++) {
            printf("double_ptr[%d] = %.2lf\n", i, double_ptr[i]);
        }
    }
    return 0;
};

int dynamic_alloc(void** ptr, int size, alloc_type_t type) {

    if(ALLOC_INT == type) {
        *ptr = TYPE_ALLOC(int, size);
    } else if(ALLOC_CHAR == type) {
        *ptr = TYPE_ALLOC(char, size);
    } else if(ALLOC_FLOAT == type) {
        *ptr = TYPE_ALLOC(float, size);
    } else if(ALLOC_DOUBLE == type) {
        *ptr = TYPE_ALLOC(double, size);
    } else {
        printf("Invalid allocation type\n");
        return -1;
    }

    return 0;
}