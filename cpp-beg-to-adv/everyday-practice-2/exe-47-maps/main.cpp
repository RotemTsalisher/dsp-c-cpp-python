#include <iostream>
#include <map>
#include <algorithm>
#include <string>
#include <cstdint>

void set_offset(std::map<std::string, std::uint32_t>& m, std::string const& name, std::uint32_t address) {
    m.insert(std::pair<std::string, std::uint32_t>(name, address));
};

int main() {

    std::map<std::string, std::uint32_t> m;

    set_offset(m, "one", 1);
    set_offset(m, "two", 2);
    set_offset(m, "three", 3);

    std::cout << "MAP:" << std::endl;
    /*
    auto it = m.begin();
    
    while(it != m.end()) {
        std::cout << it->first << " = " << it->second << std::endl;
        ++it;
    };*/

    for (auto& [k, v] : m) {
        std::cout << k << " = " << v << std::endl;
    };

    std::cout << std::endl;
    return 0;
}