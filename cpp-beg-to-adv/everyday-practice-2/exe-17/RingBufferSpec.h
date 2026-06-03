#ifndef __RINGBUFFERSPEC__H
#define __RINGBUFFERSPEC__H

#include <iostream>

class RingBufferSpec {
    private:
        int capacity_;

    public:
        RingBufferSpec() : capacity_(1024) {};
        explicit RingBufferSpec(int capacity) : capacity_(capacity) {};
        int get_capacity() const {
            return capacity_;
        };
};

#endif