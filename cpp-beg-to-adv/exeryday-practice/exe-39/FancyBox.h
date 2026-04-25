#ifndef __FANCYBOX__H
#define __FANCYBOX__H

#include "Box.h"

class FancyBox : public Box {
    public:
        int id() const;
        int v_id() const override;
};

#endif