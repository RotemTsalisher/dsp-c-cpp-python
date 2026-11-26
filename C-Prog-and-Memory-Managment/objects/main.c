#include <stdio.h>
#include "snekLib.h"

static void print_object(const char *label, const snek_object_t *obj) {
    if (obj == NULL) {
        printf("%s: NULL\n", label);
        return;
    }

    switch (obj->type) {
        case INT:
            printf("%s: INT(%d)\n", label, obj->data.int_v);
            break;
        case FLOAT:
            printf("%s: FLOAT(%g)\n", label, (double)obj->data.float_v);
            break;
        case STR:
            printf("%s: STR(\"%s\") length=%d\n",
                   label,
                   obj->data.string_v != NULL ? obj->data.string_v : "(null)",
                   snek_length((snek_object_t *)obj));
            break;
        case VECTOR:
            printf("%s: VECTOR(", label);
            for (int i = 0; i < 3; ++i) {
                snek_object_t *component = i == 0 ? obj->data.vector_v.x
                                         : i == 1 ? obj->data.vector_v.y
                                         : obj->data.vector_v.z;
                if (i != 0) printf(", ");
                if (component == NULL) {
                    printf("NULL");
                } else if (component->type == INT) {
                    printf("INT(%d)", component->data.int_v);
                } else if (component->type == FLOAT) {
                    printf("FLOAT(%g)", (double)component->data.float_v);
                } else {
                    printf("TYPE(%d)", component->type);
                }
            }
            printf(") length=%d\n", snek_length((snek_object_t *)obj));
            break;
        case ARRAY:
            printf("%s: ARRAY size=%d [", label, obj->data.array_v.size);
            for (int i = 0; i < obj->data.array_v.size; ++i) {
                snek_object_t *item = snek_array_get(obj, i);
                if (i != 0) printf(", ");
                if (item == NULL) {
                    printf("NULL");
                } else if (item->type == INT) {
                    printf("INT(%d)", item->data.int_v);
                } else if (item->type == FLOAT) {
                    printf("FLOAT(%g)", (double)item->data.float_v);
                } else if (item->type == STR) {
                    printf("STR(\"%s\")",
                           item->data.string_v != NULL ? item->data.string_v : "(null)");
                } else {
                    printf("TYPE(%d)", item->type);
                }
            }
            printf("] length=%d\n", snek_length((snek_object_t *)obj));
            break;
        default:
            printf("%s: UNKNOWN TYPE(%d)\n", label, obj->type);
            break;
    }
}

static void test_add(const char *label,
                     const snek_object_t *a,
                     const snek_object_t *b) {
    snek_object_t *result = snek_add(a, b);
    printf("[ADD] %s: ", label);
    if (result == NULL) {
        printf("NULL\n");
    } else if (result->type == INT) {
        printf("INT(%d)\n", result->data.int_v);
    } else if (result->type == FLOAT) {
        printf("FLOAT(%g)\n", (double)result->data.float_v);
    } else if (result->type == STR) {
        printf("STR(\"%s\")\n",
               result->data.string_v != NULL ? result->data.string_v : "(null)");
    } else if (result->type == VECTOR || result->type == ARRAY) {
        printf("\n");
        print_object("result", result);
    } else {
        printf("UNKNOWN TYPE(%d)\n", result->type);
    }

    refcount_dec(result);
}

static int check_refcount(const char *label,
                          const snek_object_t *obj,
                          int expected) {
    int actual = obj != NULL ? obj->refcount : -1;
    int passed = obj != NULL && actual == expected;

    printf("[REFCOUNT] %s: %s (expected %d, got %d)\n",
           label,
           passed ? "PASS" : "FAIL",
           expected,
           actual);
    return passed ? 0 : 1;
}

static int test_refcount_gc(void) {
    int failures = 0;
    printf("\n[REFCOUNT / GARBAGE COLLECTION]\n");

    snek_object_t *scalar = new_snek_int(7);
    if (scalar == NULL) {
        printf("[REFCOUNT] scalar allocation: FAIL\n");
        return 1;
    }

    failures += check_refcount("new scalar starts at 1", scalar, 1);
    refcount_inc(scalar);
    failures += check_refcount("increment raises count to 2", scalar, 2);
    refcount_dec(scalar);
    failures += check_refcount("decrement lowers count to 1", scalar, 1);
    refcount_dec(scalar);

    snek_object_t *array = new_snek_array(1);
    snek_object_t *old_value = new_snek_int(10);
    snek_object_t *new_value = new_snek_int(20);
    if (array == NULL || old_value == NULL || new_value == NULL) {
        printf("[REFCOUNT] array test allocation: FAIL\n");
        refcount_dec(array);
        refcount_dec(old_value);
        refcount_dec(new_value);
        return failures + 1;
    }

    failures += check_refcount("new array starts at 1", array, 1);
    if (snek_array_set(array, 0, old_value) != 0) {
        printf("[REFCOUNT] storing first array value: FAIL\n");
        refcount_dec(array);
        refcount_dec(old_value);
        refcount_dec(new_value);
        return failures + 1;
    }
    failures += check_refcount("array retains stored value", old_value, 2);

    if (snek_array_set(array, 0, new_value) != 0) {
        printf("[REFCOUNT] replacing array value: FAIL\n");
        refcount_dec(array);
        refcount_dec(old_value);
        refcount_dec(new_value);
        return failures + 1;
    }
    failures += check_refcount("replacement releases old array reference",
                               old_value,
                               1);
    failures += check_refcount("replacement is retained by array",
                               new_value,
                               2);
    refcount_dec(old_value);
    old_value = NULL;

    refcount_dec(new_value);
    new_value = NULL;
    snek_object_t *borrowed_value = snek_array_get(array, 0);
    if (snek_array_set(array, 0, borrowed_value) != 0) {
        printf("[REFCOUNT] self-assignment of borrowed value: FAIL\n");
        refcount_dec(array);
        return failures + 1;
    }
    failures += check_refcount("self-assignment preserves array-only reference",
                               borrowed_value,
                               1);

    refcount_inc(borrowed_value);
    refcount_dec(array);
    array = NULL;
    failures += check_refcount("freeing array releases its value",
                               borrowed_value,
                               1);
    refcount_dec(borrowed_value);
    borrowed_value = NULL;

    snek_object_t *x = new_snek_int(1);
    snek_object_t *y = new_snek_float(2.0f);
    snek_object_t *z = new_snek_int(3);
    if (x == NULL || y == NULL || z == NULL) {
        printf("[REFCOUNT] vector component allocation: FAIL\n");
        refcount_dec(x);
        refcount_dec(y);
        refcount_dec(z);
        return failures + 1;
    }

    snek_object_t *vector = new_snek_vector(x, y, z);
    if (vector == NULL) {
        printf("[REFCOUNT] vector allocation: FAIL\n");
        refcount_dec(x);
        refcount_dec(y);
        refcount_dec(z);
        return failures + 1;
    }

    failures += check_refcount("vector retains x", x, 2);
    failures += check_refcount("vector retains y", y, 2);
    failures += check_refcount("vector retains z", z, 2);
    refcount_dec(vector);
    failures += check_refcount("freeing vector releases x", x, 1);
    failures += check_refcount("freeing vector releases y", y, 1);
    failures += check_refcount("freeing vector releases z", z, 1);
    refcount_dec(x);
    refcount_dec(y);
    refcount_dec(z);

    printf("[REFCOUNT] Summary: %s (%d failure(s))\n",
           failures == 0 ? "PASS" : "FAIL",
           failures);
    return failures;
}

int main(void) {
    printf("=== SNEK LIBRARY TEST LOG ===\n");

    printf("\n[CONSTRUCTORS]\n");
    snek_object_t *int_obj = new_snek_int(42);
    snek_object_t *float_obj = new_snek_float(-3.25f);
    snek_object_t *string_obj = new_snek_string("snek");
    snek_object_t *empty_string_obj = new_snek_string("");
    snek_object_t *null_string_obj = new_snek_string(NULL);
    snek_object_t *zero_array = new_snek_array(0);
    snek_object_t *negative_array = new_snek_array(-3);
    snek_object_t *normal_array = new_snek_array(4);

    print_object("new_snek_int", int_obj);
    print_object("new_snek_float", float_obj);
    print_object("new_snek_string", string_obj);
    print_object("new_snek_string(empty)", empty_string_obj);
    print_object("new_snek_string(NULL)", null_string_obj);
    print_object("new_snek_array(0)", zero_array);
    print_object("new_snek_array(-3)", negative_array);

    snek_object_t *vector_obj = new_snek_vector(
        new_snek_int(1),
        new_snek_float(2.5f),
        new_snek_int(3)
    );
    snek_object_t *null_vector_obj = new_snek_vector(NULL, NULL, NULL);
    print_object("new_snek_vector", vector_obj);
    print_object("new_snek_vector(NULLs)", null_vector_obj);

    printf("\n[LENGTH]\n");
    printf("INT length=%d\n", snek_length(int_obj));
    printf("FLOAT length=%d\n", snek_length(float_obj));
    printf("STRING length=%d\n", snek_length(string_obj));
    printf("EMPTY STRING length=%d\n", snek_length(empty_string_obj));
    printf("VECTOR length=%d\n", snek_length(vector_obj));
    printf("ARRAY length=%d\n", snek_length(normal_array));
    printf("NULL length=%d\n", snek_length(NULL));

    printf("\n[ADDITION - SCALARS]\n");
    snek_object_t *int_a = new_snek_int(20);
    snek_object_t *int_b = new_snek_int(22);
    snek_object_t *float_a = new_snek_float(1.5f);
    snek_object_t *float_b = new_snek_float(2.25f);
    snek_object_t *mixed_float_a = new_snek_float(-0.5f);

    test_add("INT + INT", int_a, int_b);
    test_add("INT + FLOAT", int_a, float_a);
    test_add("FLOAT + INT", float_a, int_b);
    test_add("FLOAT + FLOAT", float_a, float_b);
    test_add("INT + STRING", int_a, string_obj);
    test_add("STRING + INT", string_obj, int_a);
    test_add("FLOAT + STRING", mixed_float_a, string_obj);
    test_add("STRING + FLOAT", string_obj, mixed_float_a);
    test_add("NULL + INT", NULL, int_a);
    test_add("INT + NULL", int_a, NULL);
    test_add("NULL + NULL", NULL, NULL);

    printf("\n[ADDITION - STRINGS]\n");
    snek_object_t *string_a = new_snek_string("hello ");
    snek_object_t *string_b = new_snek_string("snek");
    snek_object_t *string_empty = new_snek_string("");
    test_add("STRING + STRING", string_a, string_b);
    test_add("EMPTY + STRING", string_empty, string_b);
    test_add("STRING + EMPTY", string_b, string_empty);
    test_add("EMPTY + EMPTY", string_empty, string_empty);

    printf("\n[ADDITION - VECTORS]\n");
    snek_object_t *vector_a = new_snek_vector(
        new_snek_int(1),
        new_snek_float(2.5f),
        new_snek_int(3)
    );
    snek_object_t *vector_b = new_snek_vector(
        new_snek_int(4),
        new_snek_float(5.5f),
        new_snek_int(6)
    );
    snek_object_t *vector_mixed = new_snek_vector(
        new_snek_float(0.5f),
        new_snek_int(10),
        new_snek_float(-1.5f)
    );
    test_add("VECTOR + VECTOR", vector_a, vector_b);
    test_add("VECTOR + STRING", vector_a, string_a);
    test_add("NULL VECTOR + VECTOR", null_vector_obj, vector_a);
    test_add("VECTOR + VECTOR(MIXED TYPES)", vector_a, vector_mixed);

    printf("\n[ARRAY SET/GET]\n");
    snek_object_t *array_a = new_snek_array(4);
    snek_object_t *array_b = new_snek_array(3);
    snek_object_t *items[] = {
        new_snek_int(10),
        new_snek_float(20.5f),
        new_snek_string("third"),
        new_snek_int(40)
    };

    printf("set arrayA[0]=INT(10): %d\n",
           snek_array_set(array_a, 0, items[0]));
    printf("set arrayA[1]=FLOAT(20.5): %d\n",
           snek_array_set(array_a, 1, items[1]));
    printf("set arrayA[2]=STRING(third): %d\n",
           snek_array_set(array_a, 2, items[2]));
    printf("set arrayA[3]=INT(40): %d\n",
           snek_array_set(array_a, 3, items[3]));
    printf("set negative index: %d\n",
           snek_array_set(array_a, -1, items[0]));
    printf("set out-of-range index: %d\n",
           snek_array_set(array_a, 4, items[0]));
    printf("set NULL array: %d\n",
           snek_array_set(NULL, 0, items[0]));
    printf("set NULL value: %d\n",
           snek_array_set(array_a, 0, NULL));
    printf("set on negative array: %d\n",
           snek_array_set(negative_array, 0, items[0]));

    print_object("arrayA", array_a);
    printf("get arrayA[0]: ");
    print_object("item", snek_array_get(array_a, 0));
    printf("get arrayA[3]: ");
    print_object("item", snek_array_get(array_a, 3));
    printf("get negative index: ");
    print_object("item", snek_array_get(array_a, -1));
    printf("get out-of-range index: ");
    print_object("item", snek_array_get(array_a, 4));
    printf("get from NULL array: ");
    print_object("item", snek_array_get(NULL, 0));
    printf("get from NULL backing array: ");
    print_object("item", snek_array_get(negative_array, 0));

    printf("\n[ARRAY ADDITION]\n");
    snek_object_t *b_items[] = {
        new_snek_int(50),
        new_snek_float(60.5f),
        new_snek_string("sixth")
    };
    for (int i = 0; i < 3; ++i) {
        snek_array_set(array_b, i, b_items[i]);
    }

    print_object("arrayB", array_b);
    test_add("ARRAY + ARRAY", array_a, array_b);
    test_add("ARRAY + INT", array_a, int_a);
    test_add("INT + ARRAY", int_a, array_a);
    test_add("EMPTY ARRAY + ARRAY", zero_array, array_b);
    test_add("ARRAY + EMPTY ARRAY", array_a, zero_array);
    test_add("NEGATIVE ARRAY + ARRAY", negative_array, array_b);
    test_add("NULL ARRAY + ARRAY", NULL, array_b);

    printf("\n[CROSS-TYPE ADDITION]\n");
    test_add("ARRAY + STRING", array_a, string_a);
    test_add("STRING + VECTOR", string_a, vector_a);
    test_add("VECTOR + FLOAT", vector_a, float_a);

    int refcount_failures = test_refcount_gc();

    printf("\n=== END SNEK LIBRARY TEST LOG ===\n");
    return refcount_failures == 0 ? 0 : 1;
}
