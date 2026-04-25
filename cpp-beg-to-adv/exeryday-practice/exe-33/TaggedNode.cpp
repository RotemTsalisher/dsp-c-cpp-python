#include "TaggedNode.h"

TaggedNode::TaggedNode() : Node(), tag(0) {};
TaggedNode::TaggedNode(double x, int t) : Node(x), tag(t) {};
TaggedNode::TaggedNode(const TaggedNode& o) : Node(o.v), tag(o.tag) {};
