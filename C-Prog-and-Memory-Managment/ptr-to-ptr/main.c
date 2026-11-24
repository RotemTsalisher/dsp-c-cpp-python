#include <stdio.h>
#include <stdlib.h>

struct token {
    int id;
    float value;
};

typedef struct token token_t;

char** array_of_names(int size);
void free_array_of_names(char** names, int size);
token_t** array_of_token_ptrs(token_t* input_arr, int size);

static token_t tokens[] = {
        {1, 10.5f},
        {2, 20.25f},
        {3, 30.75f},
        {4, 40.0f}
    };

int main() {
    int size = sizeof(tokens) / sizeof(tokens[0]);

    token_t** token_ptrs = array_of_token_ptrs(tokens, size);

    for (int i = 0; i < size; ++i) {
        printf("token_ptrs[%d] -> id = %d, value = %.2f\n",
               i,
               token_ptrs[i]->id,
               token_ptrs[i]->value);
    }

    /* Free each token you allocated */
    for (int i = 0; i < size; ++i) {
        free(token_ptrs[i]);
    }

    /* Free the array of pointers */
    free(token_ptrs);

    return 0;
}

char** array_of_names(int size) {
    
    char** names = (char**)malloc(sizeof(char*) * size);
    for(int i = 0; i < size; ++i) {
        names[i] = "this is a name";
    };

    return names;
}

void free_array_of_names(char** names, int size) {
    for(int i = 0; i < size; ++i) {
        free(names[i]);
    }
    free(names);
};

token_t** array_of_token_ptrs(token_t* input_arr, int size) {
    
    token_t** array_of_tokens = (token_t**)malloc(sizeof(token_t*) * size);
    for(int i = 0; i < size; ++i) {
        array_of_tokens[i] = (token_t*)malloc(sizeof(token_t) * 1);
        *(array_of_tokens[i]) = input_arr[i];
    };

    return array_of_tokens;
};