
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
/* start types declaration */

enum snek_obj_kind {
    INT,
    FLOAT,
    BOOL
};

struct snek_int {
    char *name;
    int val;
};

struct snek_float {
    char *name;
    float val;
};

struct snek_bool {
    char *name;
    unsigned int val;
};

typedef enum snek_obj_kind snek_obj_kind_t;
typedef struct snek_int    snek_int_t;
typedef struct snek_float  snek_float_t;
typedef struct snek_bool   snek_bool_t;

/* end types declaration */

///////////////////////////

/* function declaration */

void print_value(void *data, snek_obj_kind_t type);
void init_value(void *data, snek_obj_kind_t type);
void set_value(void *data, snek_obj_kind_t type, const void* val);
void swap_strings(char** str1, char** str2);
void swap_structs(void* a, void* b, int size);