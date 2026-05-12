#include <iostream>
#include <map>
#include <unordered_map>
#include <string>

std::string vec[5] = {"Rotem", "David", "David", "David", "Rotem"};

int main() {
    
    std::map<std::string, int> map_;
    for(std::string name_ : vec) {
        map_[name_]++;
    };

    std::map<std::string, int>::iterator it = map_.begin();
    for(it; it != map_.end(); ++it) {
        std::cout << it->first << " : " 
        << it->second << std::endl;
    };
    return 0;
}