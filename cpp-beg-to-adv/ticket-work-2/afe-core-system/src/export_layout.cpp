#include "afe/export_layout.hpp"

namespace afe {

std::size_t export_header_size()
{
    return sizeof(PluginExportHeader);
}

} // namespace afe
