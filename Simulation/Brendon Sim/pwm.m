

function pwm1 = pwm(mess)
CA = 5; % Carrier Amplitude
duty = 50;
Carrier = CA*square(2*pi, duty);
i = length(Carrier);
for m = 1:i
    if(mess(m)>=Carrier(m))
        pwm1(m) = 1;
    else
        pwm1(m) = 0;
    end 
end

plot(pwm,x);
end
    


