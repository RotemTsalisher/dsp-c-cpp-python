#include <stddef.h>
#include <stdint.h>
#include <stdio.h>

#include "../DSPUtils.h"

struct pad_test {
    char byte;
    uint16_t two_bytes;
};

_Static_assert(
    sizeof(optimized_buffer_meta_t) < sizeof(unoptimized_buffer_meta_t),
    "OptimizedBufferMeta must be smaller than UnoptimizedBufferMeta");

int main(void)
{
    struct pad_test test = {0};

    printf("=== Padding probe ===\n");
    printf("sizeof(struct pad_test): %zu bytes\n",
           sizeof(test));
    printf("offsetof(byte):          %zu\n",
           offsetof(struct pad_test, byte));
    printf("offsetof(two_bytes):     %zu\n",
           offsetof(struct pad_test, two_bytes));
    printf("internal padding:        %zu bytes\n",
           offsetof(struct pad_test, two_bytes) -
           offsetof(struct pad_test, byte) -
           sizeof(test.byte));
    printf("tail padding:            %zu bytes\n",
           sizeof(test) -
           offsetof(struct pad_test, two_bytes) -
           sizeof(test.two_bytes));

    printf("\n=== Audio frame header ===\n");
    printf("sizeof(AudioFrameHeader): %zu bytes\n",
           sizeof(audio_frame_header_t));
    printf("sync_byte offset:         %zu\n",
           offsetof(audio_frame_header_t, sync_byte));
    printf("timestamp_ns offset:      %zu\n",
           offsetof(audio_frame_header_t, timestamp_ns));
    printf("sample_rate offset:       %zu\n",
           offsetof(audio_frame_header_t, sample_rate));
    printf("channel_count offset:     %zu\n",
           offsetof(audio_frame_header_t, channel_count));
    printf("frame_index offset:       %zu\n",
           offsetof(audio_frame_header_t, frame_index));
    print_diff_in_size();

    printf("\n=== Buffer metadata optimization ===\n");
    printf("Unoptimized size: %zu bytes\n",
           sizeof(unoptimized_buffer_meta_t));
    printf("Optimized size:   %zu bytes\n",
           sizeof(optimized_buffer_meta_t));
    printf("Reduction:        %zu bytes\n",
           sizeof(unoptimized_buffer_meta_t) -
           sizeof(optimized_buffer_meta_t));

    printf("\nUnoptimized offsets:\n");
    printf("  valid:          %zu\n",
           offsetof(unoptimized_buffer_meta_t, valid));
    printf("  max_amplitude:  %zu\n",
           offsetof(unoptimized_buffer_meta_t, max_amplitude));
    printf("  num_channls:    %zu\n",
           offsetof(unoptimized_buffer_meta_t, num_channls));
    printf("  peak_frequency: %zu\n",
           offsetof(unoptimized_buffer_meta_t, peak_frequency));
    printf("  muted:          %zu\n",
           offsetof(unoptimized_buffer_meta_t, muted));
    printf("  frame_id:       %zu\n",
           offsetof(unoptimized_buffer_meta_t, frame_id));

    printf("\nOptimized offsets:\n");
    printf("  max_amplitude:  %zu\n",
           offsetof(optimized_buffer_meta_t, max_amplitude));
    printf("  frame_id:       %zu\n",
           offsetof(optimized_buffer_meta_t, frame_id));
    printf("  num_channls:    %zu\n",
           offsetof(optimized_buffer_meta_t, num_channls));
    printf("  peak_frequency: %zu\n",
           offsetof(optimized_buffer_meta_t, peak_frequency));
    printf("  valid:          %zu\n",
           offsetof(optimized_buffer_meta_t, valid));
    printf("  muted:          %zu\n",
           offsetof(optimized_buffer_meta_t, muted));

    return 0;
}