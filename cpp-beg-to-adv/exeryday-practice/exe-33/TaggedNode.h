#ifndef __TAGGEDNODE__H
#define __TAGGEDNODE__H

#include "Node.h"

class TaggedNode : public Node {
    public:
        int tag;
        TaggedNode();
        explicit TaggedNode(double x, int t);
        TaggedNode(const TaggedNode& o);
};

#endif