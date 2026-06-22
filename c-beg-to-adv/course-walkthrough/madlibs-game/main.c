#include <stdio.h>


int main() {

    char color_[20];
    char plural_noun_[20];
    char celebrity_[20];

    printf("Enter a color : ");
    scanf("%s", color_);

    printf("Enter a plural-noun : " );
    scanf("%s", plural_noun_);

    printf("Enter a celebrity : ");
    scanf("%s", celebrity_);

    printf("Roses are %s\n", color_);
    printf("%s are blue\n", plural_noun_);
    printf("I love %s\n", celebrity_);

    return 0;
}