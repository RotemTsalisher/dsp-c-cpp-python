#ifndef __ISAMPLESINK__H
#define __ISAMPLESINK__H

class ISampleSink {
    public:
        virtual void write(double) = 0;
        virtual ~ISampleSink() = default;
};

#endif