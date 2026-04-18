#ifndef VLC_MONO_MIX_HPP
#define VLC_MONO_MIX_HPP

namespace vlc {

/// Energy-preserving stereo → mono PCM downmix for uplink (training model).
double mono_mix_down(double left, double right);

/// Ticket / legacy name (VLC-ENTRY-101) — same as `mono_mix_down`.
inline double monoMixDown(double const left, double const right)
{
    return mono_mix_down(left, right);
}

} // namespace vlc

#endif
