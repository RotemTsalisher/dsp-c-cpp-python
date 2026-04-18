#ifndef VLC_MIC_GAIN_CHAIN_HPP
#define VLC_MIC_GAIN_CHAIN_HPP

namespace vlc {

/// Fluent mic gain in linear domain (setDb chain returns *this).
class MicGainChain {
public:
    MicGainChain& set_db(double db);
    /// Ticket / factory-test name (VLC-ENTRY-104) — same as `set_db`.
    MicGainChain& setDb(double const db) { return set_db(db); }
    double linear() const;

private:
    double linear_{1.0};
};

} // namespace vlc

#endif
