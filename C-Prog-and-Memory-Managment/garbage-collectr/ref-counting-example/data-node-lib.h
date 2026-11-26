#ifndef __DATA__NODES__LIB__H
#define __DATA__NODES__LIB__H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

union data {
    int int_v;
    float float_v;
};

enum type {
    INT,
    FLOAT
};

typedef union data    node_data_t;
typedef enum type     node_type_t;
typedef unsigned int  node_refcount_t;
typedef unsigned char bool_t;

struct node {
    node_type_t type;
    node_data_t data;
    node_refcount_t refcount;
};

typedef struct node node_t;

node_t* new_node_int(int val);
node_t* new_node_float(float val);
node_t* ref_to(node_t* node);
void deref_node(node_t* deref);
bool_t  free_node(node_t* node);
bool_t  set_node_data(node_t* node, void* data);
bool_t  get_node_data(node_t* node, void* data);
node_refcount_t get_node_refcount(node_t* node);

#endif