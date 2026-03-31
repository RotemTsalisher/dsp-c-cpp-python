#include <iostream> 

template <typename T>
int processArray(T in, auto func, T out);

template <typename T>
void printArray(T array);

int main()
{
    auto add_one = [](auto a) {return a + 1;};
    auto double_ = [](auto a) {return a * 2;};
    auto square_ = [](auto a) {return a * a;};

    int int_arr[] = {1,2,3,4,5,6,7,8};
    double double_arr[] = {1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5};
    
    int out_int[std::size(int_arr)] = {0};
    double out_double[std::size(double_arr)] = {0};

    std::cout << "Original integers: ";
    printArray(int_arr);
    std::cout << std::endl;

    processArray(int_arr, double_, out_int);
    std::cout << "Doubled: ";
    printArray(out_int);
    std::cout << std::endl;

    processArray(int_arr, square_, out_int);
    std::cout << "Squared: ";
    printArray(out_int);
    std::cout << std::endl;

    std::cout << "Original doubles: ";
    printArray(double_arr);
    std::cout << std::endl;

    processArray(double_arr, add_one, out_double);
    std::cout << "Incremented: ";
    printArray(out_double);
    std::cout << std::endl;
    
    return 0;
}

template <typename T>
int processArray(T in, auto func, T out) {
    int i = 0;

    for (auto v : in)
    {
        out[i++] = func(v);
    }

    return i; // number of processed elements
};

template <typename T>
void printArray(T array){

    std::cout << "[";
    for(auto v : array)
    {
        std::cout << v << ", ";
    }
    std::cout << "]";
};
