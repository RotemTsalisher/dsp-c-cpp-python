#ifndef AFE_EXPORT_LAYOUT_HPP
#define AFE_EXPORT_LAYOUT_HPP

#include <cstddef>
#include <cstdint>

namespace afe {

#pragma pack(push, 1)
struct PluginExportHeader {
    std::uint16_t version;
    std::uint32_t flags;
};
#pragma pack(pop)

std::size_t export_header_size();

} // namespace afe

#endif
