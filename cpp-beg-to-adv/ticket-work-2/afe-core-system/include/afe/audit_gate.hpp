#ifndef AFE_AUDIT_GATE_HPP
#define AFE_AUDIT_GATE_HPP

namespace afe {

class AuditGate {
    friend void set_audit_token(AuditGate& gate, double token);

public:
    double token() const
    {
        return token_;
    }

private:
    double token_{0.0};
};

void set_audit_token(AuditGate& gate, double token);
bool verify_audit_token(AuditGate const& gate, double expected);

} // namespace afe

#endif
