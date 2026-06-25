#include <stdio.h>

int main() {
    int sample_rate_hz, delay_samples;
    double comb_delay_ms, feedback_gain;
    char uplink_mode, bench_location[64];

    printf("Enter sample rate : ");
    scanf("%d", &sample_rate_hz);

    printf("Enter comb delay [ms] : ");
    scanf("%lf", &comb_delay_ms);

    printf("Enter feedback gain : ");
    scanf("%lf", &feedback_gain);

    printf("Enter M/S [mono / stereo] : ");
    fflush(stdin);
    scanf(" %c", &uplink_mode);

    (void)getchar();
    printf("Enter bench location : ");
    fgets(bench_location, 64, stdin);


    delay_samples = sample_rate_hz * (comb_delay_ms / 1000.0);
    printf("==========\n");
    printf("Sample rate = %d\n", sample_rate_hz);
    printf("Comb delay = %5.3f\n", comb_delay_ms);
    printf("Feedback gain = %5.3f\n", feedback_gain);
    printf("Uplink mode = %c\n", uplink_mode);
    printf("Bench location = %s", bench_location);
    printf("Computed delay in samples = %d\n", delay_samples);
    
    return 0;
}