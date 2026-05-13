#include <iostream>
#include <thread>
#include <type_traits>


static bool working_ = false;
/*
double vals[] = {0.0, 1.0, 2.5, 3.1};
static double acc = 0;
*/

template <typename T, size_t N, typename Fn>
void sum_values(T (&v)[N], double &acc_, Fn fn) {
    working_ = true;
    fn(v, N, acc_);
    working_ = false;
};

int main() {
    /*
    auto sum_float = [](double v[], size_t N, double &sum_) {
        for (size_t i = 0; i < N; i++) {
            sum_ += v[i];
        };
    };*/

    double vals[] = {0.0, 1.0, 2.5, 3.1};
    double acc = 0;

    std::thread p0(sum_values<double, 4, decltype(sum_float)>,vals, acc, sum_float);

    p0.join();
    std::cout << "acc = " << acc << std::endl;
    return 0;
};
