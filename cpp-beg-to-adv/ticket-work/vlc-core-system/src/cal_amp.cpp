#include "vlc/cal_amp.hpp"

namespace vlc {

void set_factory_trim(CalAmp& a, double const v)
{
    a.trim_ = v;
}

void setFactoryTrim(CalAmp& a, double const v)
{
    a.trim_ = v;
}

} // namespace vlc
