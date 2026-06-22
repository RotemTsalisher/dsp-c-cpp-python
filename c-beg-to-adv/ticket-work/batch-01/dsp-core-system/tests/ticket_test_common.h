#ifndef DSP_TICKET_TEST_COMMON_H
#define DSP_TICKET_TEST_COMMON_H

#include <math.h>
#include <stdio.h>

static int dsp_nearly_equal(double const a, double const b, double const eps)
{
    return fabs(a - b) <= eps;
}

static int dsp_fail(char const* ticket)
{
    printf("%s FAIL\n", ticket);
    return 1;
}

static int dsp_pass(char const* ticket)
{
    printf("%s PASS\n", ticket);
    return 0;
}

static void dsp_print_header(char const* ticket, char const* title)
{
    printf("=== %s — %s ===\n", ticket, title);
}

static void dsp_print_observed(char const* label, double value)
{
    printf("  observed %s: %g\n", label, value);
}

static void dsp_print_observed_int(char const* label, int value)
{
    printf("  observed %s: %d\n", label, value);
}

static void dsp_print_observed_str(char const* label, char const* value)
{
    printf("  observed %s: %s\n", label, value);
}

static void dsp_print_expected(char const* label, double value)
{
    printf("  expected %s: %g\n", label, value);
}

static void dsp_print_expected_int(char const* label, int value)
{
    printf("  expected %s: %d\n", label, value);
}

static void dsp_print_expected_str(char const* label, char const* value)
{
    printf("  expected %s: %s\n", label, value);
}

#endif
