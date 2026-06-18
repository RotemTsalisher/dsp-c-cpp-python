#include <iostream>
#include "Stage.h"
#include "FirStage.h"

int main() {
    FirStage fstage;

    double x = 2.0;
    
    std::cout << "x = " << x << std::endl << ".25 * x = " << fstage.process(x) << std::endl;
    return 0;
}