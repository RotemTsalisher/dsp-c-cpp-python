#include <iostream>
#include <map>

int main() {
    std::multimap<int, char> mm;

    mm.insert(std::make_pair<int, char>(0, 'a'));
    mm.insert(std::make_pair<int, char>(0, 'b'));

    std::multimap<int, char>::iterator it = mm.begin();

    for(it; it != mm.end(); ++it) {
        std::cout << it->first << " : "
        << it->second << std::endl;
    };

    return 0;
    
};