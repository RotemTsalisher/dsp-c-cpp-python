#include "vlc/cal_amp.hpp"

namespace vlc {

void set_factory_trim(CalAmp& a, double const v)
{
    a.trim_ = v;
    (void)a;
    (void)v;
}

void setFactoryTrim(CalAmp& a, double const v)
{
    (void)a;
    (void)v;
}

} // namespace vlc
