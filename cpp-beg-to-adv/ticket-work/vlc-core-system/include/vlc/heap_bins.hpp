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

    /// Test hook: increments on construction; should decrement in destructor (VLC-ENTRY-103).
    static int live_instances() { return live_instances_; }

private:
    static int live_instances_;
    std::size_t const count_;
    double* bins_;
};

} // namespace vlc

#endif
