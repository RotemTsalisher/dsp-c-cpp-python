#include <iostream>
#include <map>
#include <unordered_map>

int main() {
    std::map<int, char> m;

    m[1] = 'a';
    m[1] = 'b'; // override

    m.insert(std::make_pair<int,char>(0, 'c'));
    m.insert(std::make_pair<int,char>(0, 'd')); // not inserting

    std::map<int,char>::iterator it = m.begin();
    for(it; it != m.end(); ++it){
        std::cout << it->first <<" = " << it->second <<std::endl;
    };

    std::unordered_map<int, char> u_m;
    u_m[9] = 'a';
    u_m[1] = 'b';
    u_m[5] = 'c';

    std::unordered_map<int, char>::iterator it_ = u_m.begin();
    for(it_; it_ != u_m.end(); ++it_) {
        std::cout << it_->first << " : " 
        << it_->second << std::endl;
    };
    

    return 0;

}