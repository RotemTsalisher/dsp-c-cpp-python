#include "afe/audit_gate.hpp"

namespace afe {

void set_audit_token(AuditGate& gate, double const token)
{
    (void)gate;
    (void)token;
}

bool verify_audit_token(AuditGate const& gate, double const expected)
{
    return gate.token() == expected;
}

} // namespace afe
