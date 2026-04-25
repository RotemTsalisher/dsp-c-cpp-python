#include <iostream>
#include "..\exe-34\Processor.h"
#include "..\exe-34\PassThrough.h"

double run(Processor* p, double x){
    std::cout << "Processor P: " << p->tick(x) << std::endl;
    return p->tick(x);
};

double run(PassThrough* p, double x) {
    std::cout << "PassThrough P: " << p->tick(x) << std::endl;
    return p->tick(x);
};

int main() {

    Processor *pt0 = new PassThrough;

    run(pt0, 1.0);
    std::cout << "pt0 = " << pt0->tick(100.0) << std::endl;
    std::cout << "PROCESSOT :: :: " << dynamic_cast<Processor *>(pt0)->tick(222.2);
    return 0;
};