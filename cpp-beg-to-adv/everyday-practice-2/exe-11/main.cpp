#include <iostream>
#include <type_traits>

template <typename T>
struct is_scalar_audio_sample {
    constexpr static bool v = std::is_same_v<T, float> ||
    std::is_same_v<T, double> || std::is_same_v<T, int>; 
};

template <typename T>
inline constexpr bool is_scalar_audio_sample_v = is_scalar_audio_sample<T>::v;


int main() {
    std::cout << "is_scalar_audio_sample_v<int> : " <<
    is_scalar_audio_sample_v<int> << std::endl;
    
    std::cout << "is_scalar_audio_sample_v<float> : " <<
    is_scalar_audio_sample_v<float> << std::endl;
    
    std::cout << "is_scalar_audio_sample_v<double> : " <<
    is_scalar_audio_sample_v<double> << std::endl;
    
    std::cout << "is_scalar_audio_sample_v<char> : " <<
    is_scalar_audio_sample_v<char> << std::endl;
    
    return 0;
};
