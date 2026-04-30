#include <iostream>
#include <map>
#include <unordered_map>
#include <string>

int main() {
    std::map<std::string, int> map;
    map["Rotem"] = 100;
    map["Rotem2"] = 101;
    map["Rotem3"] = 102;

    std::cout << "map[Rotem] = " << map["Rotem"] << std::endl;
    std::cout << "map[Rotem2] = " << map["Rotem2"] << std::endl;
    std::cout << "map[Rotem3] = " << map["Rotem3"] << std::endl;

    map.insert(std::make_pair<std::string, int>("TLV", 1000));
    std::cout << "map[TLV] = " << map["TLV"] << std::endl;
    
    std::map<std::string, int>::iterator it = map.begin();
    for(it; it != map.end(); ++it) {
        std::cout << "(" << it->first << ", " << it->second << ")" << std::endl;
    };
    return 0;
};