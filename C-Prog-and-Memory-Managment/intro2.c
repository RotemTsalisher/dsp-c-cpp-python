#include <stdio.h>

typedef unsigned char uint8_t;
typedef unsigned short uint16_t;
typedef unsigned int uint32_t;

#define PORT8_1 0xFA
#define PORT8_2 0xFB
#define PORT8_3 0xFC
#define PORT8_4 0xFD

#define PORT16_1 0xFAFB
#define PORT16_2 0xFCFD

#define PORT32_1 0xFCFDFAFB

union tcp_params {
    struct {
        uint16_t source_port;
        uint16_t dest_port;
    };

    uint32_t ports;
    unsigned char ports_[4];
};

typedef union tcp_params tcp_params_t;

int main() {

    tcp_params_t params_16, params_32, params_8;
    params_16.source_port = PORT16_1;  
    params_16.dest_port = PORT16_2;

    params_32.ports = PORT32_1;
    params_8.ports_[0] = PORT8_1;
    params_8.ports_[1] = PORT8_2;
    params_8.ports_[2] = PORT8_3;
    params_8.ports_[3] = PORT8_4;    

    printf("Source Port: 0x%04X\n", params_16.source_port);
    printf("Destination Port: 0x%04X\n", params_16.dest_port);
    printf("Combined Ports (32-bit): 0x%08X\n", params_16.ports);

    printf("Combined Ports (32-bit from 32-bit union): 0x%08X\n", params_32.ports);

    printf("Combined Ports (8-bit): 0x%08X\n", (0x00 | ((uint32_t)(params_8.ports_[0])<<8) | ((uint32_t)(params_8.ports_[1])) | ((uint32_t)(params_8.ports_[2]) << 24) | ((uint32_t)(params_8.ports_ [3]) << 16)) );

    return 0;
}