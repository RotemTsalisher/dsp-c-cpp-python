#include <stdio.h>
#include <stdlib.h>

#define PRINT_SAMPLE_FMT(s)  "ID : %d | Value : %4.2lf |\n", s.id, s.value
#define PRINT_SAMPLE(s)      printf(PRINT_SAMPLE_FMT(s))
#define INIT_MSG(id)         "===== INIT " #id " =====\n"

struct Sample {
    int id;
    double value;
};

int is_equal(const struct Sample *s1, const struct Sample *s2);
void init_sample(struct Sample *s);

int main() {

    struct Sample s0, s1;

    printf(INIT_MSG(s0));
    init_sample(&s0);
    
    printf(INIT_MSG(s1));
    init_sample(&s1);

    PRINT_SAMPLE(s0);
    PRINT_SAMPLE(s1);

    if(is_equal(&s0, &s1)) {
        printf("EQ\n");
    }
    else{
        printf("NE\n");
    }
    return 0;
}

int is_equal(const struct Sample *s1, const struct Sample *s2) {
    return (s1->id == s2->id && s1->value == s2->value);
};

void init_sample(struct Sample *s) {
    printf("Enter id : ");
    scanf(" %d", &(s->id));

    printf("Enter Value : ");
    scanf(" %lf", &(s->value));
};