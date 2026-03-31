#include <iostream>
#include <string>

class Greeter {
    private:
        std::string greet;

    public:
        Greeter() {
            greet = "Hello World!";
        };

        Greeter(std::string greet_) {
            greet = greet_;
        };

        void say_hello() {
            std::cout << greet << std::endl;
        };
};

int main()
{
    Greeter first_greet;
    Greeter second_greet("My name is Rotem!");

    first_greet.say_hello();

    second_greet.say_hello();
    return 0;
}