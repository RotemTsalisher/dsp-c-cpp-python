#ifndef VLC_HEAP_BINS_HPP
#define VLC_HEAP_BINS_HPP

#include <cstddef>

namespace vlc {

/// Owns a heap-allocated PSD bin buffer (fixed count at construction).
class HeapBins {
public:
    explicit HeapBins(std::size_t bin_count);
    ~HeapBins();

    HeapBins(HeapBins const&) = delete;
    HeapBins& operator=(HeapBins const&) = delete;

    double* data();
    double const* data() const;
    std::size_t size() const;

private:
    std::size_t const count_;
    double* bins_;
};

} // namespace vlc

#endif
