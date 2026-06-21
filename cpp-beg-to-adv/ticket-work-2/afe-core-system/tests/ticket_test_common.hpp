#ifndef AFE_TICKET_TEST_COMMON_HPP
#define AFE_TICKET_TEST_COMMON_HPP

#include <cmath>
#include <iostream>
#include <string>

namespace afe::test {

inline bool nearly_equal(double const a, double const b, double const eps = 1e-9)
{
    return std::abs(a - b) <= eps;
}

inline int fail(std::string const& ticket)
{
    std::cout << ticket << " FAIL\n";
    return 1;
}

inline int pass(std::string const& ticket)
{
    std::cout << ticket << " PASS\n";
    return 0;
}

inline void print_header(std::string const& ticket, std::string const& title)
{
    std::cout << "=== " << ticket << " — " << title << " ===\n";
}

inline void print_observed(std::string const& label, auto const& value)
{
    std::cout << "  observed " << label << ": " << value << '\n';
}

inline void print_expected(std::string const& label, auto const& value)
{
    std::cout << "  expected " << label << ": " << value << '\n';
}

} // namespace afe::test

#endif
