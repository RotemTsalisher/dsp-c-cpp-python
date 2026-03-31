template <typename F, typename T>
class MathEngine {
    private:
        F func;
    
    public:
        MathEngine() = default;
        MathEngine(F func_);

        void apply_(T &num);
};

template <class F, typename T>
MathEngine<F,T>::MathEngine(F func_) : func(func_) {};

template <class F, typename T>
void MathEngine<F,T>::apply_(T &num) {
    func(num);
};