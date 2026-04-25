#include <iostream>
#include "HeapBins.h"

int main() {

    HeapBins hb0;
    HeapBins hb1(3);

    hb0.print_bins();

    hb1.set_bin(1,0).set_bin(2,1).set_bin(3,2);
    hb1.print_bins();
    return 0;
};