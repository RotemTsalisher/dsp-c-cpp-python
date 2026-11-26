#include <stdio.h>
#include <stdlib.h>
#include "data-node-lib.h"

static int passed;
static int failed;

static void check(const char *name, int condition) {
    printf("[%s] %s\n", condition ? "PASS" : "FAIL", name);
    if (condition) {
        ++passed;
    } else {
        ++failed;
    }
}

int main(void) {
    node_t *int_node = new_node_int(42);
    node_t *float_node = new_node_float(1.25f);

    check("new_node_int returns a node", int_node != NULL);
    check("new_node_float returns a node", float_node != NULL);

    if (int_node == NULL || float_node == NULL) {
        if (int_node != NULL) {
            free_node(int_node);
        }
        if (float_node != NULL) {
            free_node(float_node);
        }
        printf("Cannot continue: node allocation failed.\n");
        return EXIT_FAILURE;
    }

    check("new nodes start with refcount 1",
          get_node_refcount(int_node) == 1 &&
          get_node_refcount(float_node) == 1);
    check("NULL refcount is 0", get_node_refcount(NULL) == 0);

    int int_value = 0;
    float float_value = 0.0f;

    check("get_node_data reads INT",
          get_node_data(int_node, &int_value) == 0 && int_value == 42);
    check("get_node_data reads FLOAT",
          get_node_data(float_node, &float_value) == 0 &&
          float_value == 1.25f);

    int new_int_value = 99;
    float new_float_value = -2.5f;

    check("set_node_data updates INT",
          set_node_data(int_node, &new_int_value) == 0 &&
          get_node_data(int_node, &int_value) == 0 &&
          int_value == new_int_value);
    check("set_node_data updates FLOAT",
          set_node_data(float_node, &new_float_value) == 0 &&
          get_node_data(float_node, &float_value) == 0 &&
          float_value == new_float_value);

    check("set_node_data rejects NULL node",
          set_node_data(NULL, &new_int_value) != 0);
    check("set_node_data rejects NULL data",
          set_node_data(int_node, NULL) != 0);
    check("get_node_data rejects NULL node",
          get_node_data(NULL, &int_value) != 0);
    check("get_node_data rejects NULL data",
          get_node_data(int_node, NULL) != 0);

    node_type_t saved_type = int_node->type;
    int_node->type = (node_type_t)2;
    check("set_node_data rejects unsupported type",
          set_node_data(int_node, &new_int_value) != 0);
    check("get_node_data rejects unsupported type",
          get_node_data(int_node, &int_value) != 0);
    int_node->type = saved_type;

    node_t *int_ref = ref_to(int_node);
    check("ref_to returns the same node", int_ref == int_node);
    check("ref_to increments refcount to 2",
          get_node_refcount(int_node) == 2);
    check("ref_to rejects NULL", ref_to(NULL) == NULL);

    deref_node(NULL);
    check("deref_node(NULL) leaves count unchanged",
          get_node_refcount(int_node) == 2);

    deref_node(int_ref);
    check("deref_node decrements count to 1",
          get_node_refcount(int_node) == 1);

    check("free_node(NULL) reports failure", free_node(NULL) != 0);
    check("free_node releases a node", free_node(float_node) == 0);

    deref_node(int_node);
    printf("[INFO] Final dereference called; node should now be released.\n");

    printf("\nResults: %d passed, %d failed\n", passed, failed);
    return failed == 0 ? EXIT_SUCCESS : EXIT_FAILURE;
}