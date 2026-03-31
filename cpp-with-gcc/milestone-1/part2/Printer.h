#include <iostream>
#include <tuple>

template <typename... Args>
class Printer {
    private:
        std::tuple<Args...> args;
    
    public:

        Printer(Args... args_) : args(args_...) {
            std::cout << "Parametric Constructor" << std::endl;
        };

        void print_stored_vals() {
            std::apply([](const Args&... vals) { ((std::cout << vals << " " ), ... ); }, args); 
            std::cout << std::endl;
        };
};
