#include <iostream>
#include "../exe-16/PsdAccumulator.h"

int main() {
    PsdAccumulator* psdAcc;
    psdAcc = new PsdAccumulator;

    psdAcc->push(1.5);

    double sum_sq = psdAcc->get_sumSq();
    std::cout << "sum_sq = " << sum_sq << std::endl;

    psdAcc->push(1);
    sum_sq = psdAcc->get_sumSq();
    std::cout << "sum_sq = " << sum_sq << std::endl;

    delete psdAcc;

    return 0;
};