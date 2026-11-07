#include <stdio.h>

#define CLEAR_BIT(v, bit)    ((v) &= ~(0x01 << bit))
#define SET_BIT(v, bit)      ((v) |= (0x01 << bit))
#define TOGGLE_BIT(v, bit)   ((v) ^= (0x01 << bit))
#define READ_BIT(v,bit)      ((v) & (0x01 << bit))

#define READY_BIT            (0x01 << 7)
#define HIGH_ADC             (0x01)
#define MID_ADC              (0x1A)
#define LOW_ADC              (0xdf)
            
typedef unsigned char uint_8;

typedef struct {
    uint_8 mode     : 2;
    uint_8 enable   : 1;
    uint_8 address  : 5;
} control_reg;

void exe_1(int *vec);
void exe_2(uint_8 *vec);
void exe_3(uint_8 high, uint_8 mid, uint_8 low, int *res);
void exe_4(control_reg* cr);
int is_power_of_two(unsigned int n);
int abs_val(int n);
int multiply_sensor_val(int sensor_val);

static uint_8 SR_REG = 0x01;

int main() {
    
    control_reg cr;
    exe_4(&cr);

    printf("enable 0x%x || mode 0x%x || address 0x%x\n", cr.enable, cr.mode, cr.address);

    return 0;
}

void exe_1(int *vec) {

    for(int i = 4; i < 7; ++i) {
        CLEAR_BIT(*vec, i);
    };

    SET_BIT(*vec, 4);
    SET_BIT(*vec, 6);
}

void exe_2(uint_8 *vec) {
    while(!(*vec == READY_BIT)) {
        printf("vec = 0x%x\n", (*vec));
        (*vec) = (*vec << 1);
        printf("STUCK IN WHILE..\n");
    };

    printf("DONE!\n");
}

void exe_3(uint_8 high, uint_8 mid, uint_8 low, int *res) { 

    *res = 0; // clear
    uint_8 sign_ = READ_BIT(high, 7);

    for(int i = 0; i < 7; ++i) {
        sign_ |= (sign_ >> 1);
    };

    printf("sign_ = 0x%x\n", sign_);

    *res |= ((int)low);
    *res |= ((int)mid << 8);
    *res |= ((int)high << 16);
    *res |= ((int)sign_ << 24);
}

void exe_4(control_reg* cr) {
    
    cr->mode    = 0x01;
    cr->enable  = 0x01;
    cr->address = 18; 
};

int is_power_of_two(unsigned int n) {
    return ( n && !(n & (n - 1)) );
};

int abs_val(int n) {
    int sign_ = n >> 31;
    return (n + sign_)^sign_;
    // if sign_ = 0, do nothing
    // if sign_ = -1, than it's subtracting 1 from a negative, and flipping all bits
    // which basically is giving the positive number
}

int multiply_sensor_val(int sensor_val) {
    return ((sensor_val * 3) >> 1);
};