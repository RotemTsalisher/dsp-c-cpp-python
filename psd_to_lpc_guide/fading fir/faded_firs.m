h1 = fir1(64, 0.2);
h2 = fir1(64, 0.6);

x = randn(1,2000);

y1 = filter(h1,1,x)';
y2 = filter(h2,1,x)';

Nfade = 512;
alpha = [linspace(0,1,Nfade), ones(1, length(x) - length(Nfade))];

y = (1 - alpha).*y1 + alpha.*y2;

plot(alpha)