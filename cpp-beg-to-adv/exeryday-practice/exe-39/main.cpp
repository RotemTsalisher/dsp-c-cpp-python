#include <iostream>
#include "Box.h"
#include "FancyBox.h"

int main() {
    Box *b = new FancyBox();

    std::cout << "id() = " << b->id() << std::endl;
    std::cout << "v_id() = " << b->v_id() << std::endl;
    return 0;
};