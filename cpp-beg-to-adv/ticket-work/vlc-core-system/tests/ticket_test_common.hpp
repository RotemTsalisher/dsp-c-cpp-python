#ifndef VLC_TICKET_TEST_COMMON_HPP
#define VLC_TICKET_TEST_COMMON_HPP

#include <cmath>
#include <cstdlib>
#include <iostream>
#include <string>

namespace vlc::test {

inline bool nearly_equal(double const a, double const b, double const eps = 1e-9)
{
    return std::abs(a - b) <= eps;
}

inline int fail(std::string const& ticket, std::string const& message)
{
    std::cout << ticket << " FAIL (bug still present)\n"
              << "  " << message << '\n';
    return 1;
}

inline int pass(std::string const& ticket, std::string const& message)
{
    std::cout << ticket << " PASS\n"
              << "  " << message << '\n';
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
    std::cout << "  expected " << label << ": " << value << " (after your fix)\n";
}

} // namespace vlc::test

#endif
