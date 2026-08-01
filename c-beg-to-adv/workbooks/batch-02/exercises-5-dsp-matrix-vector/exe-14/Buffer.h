#ifndef __BUFFER__H
#define __BUFFER__H

#include <iostream>

static constexpr size_t MAX_BUFF_SIZE = 100;
class Buffer {
    private:
        double buff[MAX_BUFF_SIZE];
        size_t l;

    public:
        Buffer() = default;
        Buffer(const double *b, size_t l_);
        Buffer(const Buffer& other);
        ~Buffer() = default;

        const double& operator[](size_t i) const;
        double& operator[](size_t i);
        void compute_energy(double& energy_l, double& energy_r) const;
        void write_mono(Buffer& mono_buffer) const;
        friend std::ostream& operator<<(std::ostream& os, const Buffer& buff);
};

#endif