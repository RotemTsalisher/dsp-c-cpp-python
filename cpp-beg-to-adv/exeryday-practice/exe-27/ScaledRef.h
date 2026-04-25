#ifndef __SCALEDREF__H
#define __SCALEDREF__H

class ScaledRef {
    private:
        double const scale_;
        double const& ref_;
    public:
        ScaledRef();
        ScaledRef(double scale, double ref);
        double get_scale() const;
        double get_ref() const;

        
};

#endif