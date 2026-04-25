#include <iostream>
#include "Node.h"
#include "TaggedNode.h"

int main() {
    TaggedNode tn(1.25, 1);
    TaggedNode other_tn(tn);

    std::cout << "other_tn = " << other_tn.v << ", " << other_tn.tag << std::endl;

    return 0;
};