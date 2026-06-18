#ifndef __STAGE__H
#define __STAGE__H

class Stage {
    public:
        virtual double process(double x) = 0;
        virtual ~Stage() = default;
};

#endif