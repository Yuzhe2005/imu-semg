function [iemg0_env, iemg1_env, iemg2_env, iemg3_env] = calculate_IEMG(data_path, window_ms, varargin)

fs = 1300;             

if ~(isscalar(window_ms) && window_ms > 0)
    error('calculate_IEMG:BadWindow', 'window_ms must be positive');
end

window_size = round(window_ms * fs / 1000);

if window_size < 1
    window_size = 1;
end

[EMGA0, EMGA1, EMGA2, EMGA3] = plot_MyowareData(data_path, varargin{:});


abs0 = abs(EMGA0);
abs1 = abs(EMGA1);
abs2 = abs(EMGA2);
abs3 = abs(EMGA3);

iemg0_env = movsum(abs0, [window_size-1, 0]);
iemg1_env = movsum(abs1, [window_size-1, 0]);
iemg2_env = movsum(abs2, [window_size-1, 0]);
iemg3_env = movsum(abs3, [window_size-1, 0]);

N = length(iemg0_env);          
t = (0:(N-1)) / fs;       

figure;
subplot(2,2,1)
plot(t, iemg0_env);
title('Channel A0 IEMG');
xlabel('Time (s)');
ylabel('IEMG');
grid on

subplot(2,2,2)
plot(t, iemg1_env);
title('Channel A1 IEMG');
xlabel('Time (s)');
ylabel('IEMG');
grid on

subplot(2,2,3)
plot(t, iemg2_env);
title('Channel A2 IEMG');
xlabel('Time (s)');
ylabel('IEMG');
grid on

subplot(2,2,4)
plot(t, iemg3_env);
title('Channel A3 IEMG');
xlabel('Time (s)');
ylabel('IEMG');
grid on

end
