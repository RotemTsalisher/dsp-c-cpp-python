#ifndef __FIFOCHANNEL__H
#define __FIFOCHANNEL__H

class FifoChannel {
    private:
        int depth_;
    public:
        int depth() const;
        FifoChannel() : depth_(0) {};
};

#endif