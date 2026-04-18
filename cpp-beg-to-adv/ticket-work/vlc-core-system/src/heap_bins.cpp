#include "vlc/heap_bins.hpp"

#include <new>
#include <stdexcept>

namespace vlc {

HeapBins::HeapBins(std::size_t const bin_count)
    : count_{bin_count}
    , bins_{nullptr}
{
    if (count_ == 0) {
        throw std::invalid_argument("bin_count");
    }
    bins_ = new double[count_]{};
}

HeapBins::~HeapBins()
{
    delete[] bins_;
}

double* HeapBins::data()
{
    return bins_;
}

double const* HeapBins::data() const
{
    return bins_;
}

std::size_t HeapBins::size() const
{
    return count_;
}

} // namespace vlc
