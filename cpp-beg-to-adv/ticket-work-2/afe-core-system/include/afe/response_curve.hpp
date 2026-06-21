#ifndef AFE_RESPONSE_CURVE_HPP
#define AFE_RESPONSE_CURVE_HPP

namespace afe {

struct IResponseCurve {
    virtual double eval(double x) const = 0;
    virtual ~IResponseCurve() = default;
};

class ResponseCurve final : public IResponseCurve {
public:
    double eval(double x) const override;
    double eval(double x, bool normalized) const;
};

} // namespace afe

#endif
