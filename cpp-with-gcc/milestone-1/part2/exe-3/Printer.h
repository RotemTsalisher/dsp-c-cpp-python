#include <iostream>

template <typename... Args>
class Printer {
    private:
        std::tuple<Args...> args;
    public:
        Printer(Args... args_) : args(args_...) {};
        void print_stored_values() {
            std::apply([](const Args&... args) {((std::cout << args << " "), ...);}, args);
            std::cout << std::endl;
        };
};