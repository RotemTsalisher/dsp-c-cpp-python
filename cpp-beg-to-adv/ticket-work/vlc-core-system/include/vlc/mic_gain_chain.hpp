#ifndef VLC_MIC_GAIN_CHAIN_HPP
#define VLC_MIC_GAIN_CHAIN_HPP

namespace vlc {

/// Fluent mic gain in linear domain (setDb chain returns *this).
class MicGainChain {
public:
    void set_db(double db);
    /// Ticket / factory-test name (VLC-ENTRY-104) — same as `set_db`.
    void setDb(double const db) { set_db(db); }
    double linear() const;

private:
    double linear_{1.0};
};

} // namespace vlc

#endif
