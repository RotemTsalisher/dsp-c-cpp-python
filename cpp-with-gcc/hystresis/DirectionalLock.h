#ifndef DIRECTIONAL_LOCK_H_
#define DIRECTIONAL_LOCK_H_

class DirectionalLock {
    private:
        double current;
        static double thresh;
    
    public:
        DirectionalLock() = default;
        DirectionalLock(double current_) : current(current_) {};
        DirectionalLock(const DirectionalLock& dl) : current(dl.current) {};

        void update(double input);
        double get_current();
};
#endif