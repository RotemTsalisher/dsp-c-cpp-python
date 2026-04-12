#ifndef __STREAMINGINTERFACE__H
#define __STREAMINGINTERFACE__H

#include <iostream>

class StreamingInterface {
    friend std::ostream& operator<<(std::ostream& os, const StreamingInterface& si);

    public:
        virtual void stream_insert(std::ostream out) const = 0;
};
#endif