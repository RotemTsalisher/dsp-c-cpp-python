#include <iostream>
#include <thread>
#include <type_traits>


static bool working_ = false;

double vals[] = {0.0, 1.0, 2.5, 3.1};
static double acc = 0;


template <typename T, size_t N, typename Fn>
void sum_values(T (&v)[N], double &acc_, Fn fn) {
    working_ = true;
    fn(v, N, acc_);
    working_ = false;
};

int main() {
    
    auto accumulate_ = [](double v[], size_t N, double &acc) {
        for(size_t i = 0; i< N; i++){
            acc += v[i];
        };
    };

    sum_values(vals, acc, accumulate_);
    std::cout << "acc = " << acc << std::endl;
    return 0;
};
