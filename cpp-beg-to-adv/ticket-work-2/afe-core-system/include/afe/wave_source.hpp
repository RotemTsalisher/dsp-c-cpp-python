#ifndef AFE_WAVE_SOURCE_HPP
#define AFE_WAVE_SOURCE_HPP

namespace afe {

class WaveSource {
public:
    double next_sample()
    {
        return 0.0;
    }
    virtual ~WaveSource() = default;
};

class ToneSource : public WaveSource {
public:
    double next_sample()
    {
        return 0.707;
    }
};

} // namespace afe

#endif
