#ifndef __CHANNEL__H
#define __CHANNEL__H

#include <iostream>
static constexpr size_t MAX_CHANNEL_LENGTH = 100;

class Channel {
    private:    
        double vec[100];
        size_t l;
    public:
        
        Channel() = default;
        Channel(const double *v, size_t l_);
        Channel(const Channel &other);
        ~Channel() = default;

        void operator*(double g);
        void operator+(const Channel &other);
        friend std::ostream& operator<<(std::ostream& os, const Channel& ch);
};

#endif