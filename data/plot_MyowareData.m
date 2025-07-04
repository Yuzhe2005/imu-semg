function [EMGA0, EMGA1, EMGA2, EMGA3] = plot_MyowareData(data_path, varargin)
crop_range = [5, -1];
do_plot = false;
for i = 1:2:length(varargin)
    if strcmp(varargin{i}, 'crop_range')
        crop_range = varargin{i+1};
    end

    if strcmp(varargin{i}, 'do_plot')
        do_plot = varargin{i+1};
    end
end

S = load(data_path);
% try 
%     EMGA0 = detrend(S.A0);
%     EMGA1 = detrend(S.A1);
%     EMGA2 = detrend(S.A2);
%     EMGA3 = detrend(S.A3);
% catch

try 
    EMGA0 = (S.A0);
    EMGA1 = (S.A1);
    EMGA2 = (S.A2);
    EMGA3 = (S.A3);
catch
    disp("Didn't find the sensor data")
    return
end

EMGA0 = EMGA0(crop_range(1):end+crop_range(2));
EMGA1 = EMGA1(crop_range(1):end+crop_range(2));
EMGA2 = EMGA2(crop_range(1):end+crop_range(2));
EMGA3 = EMGA3(crop_range(1):end+crop_range(2));

filter = [20, 498];
order = 4;
fs = 1300;
N = length(EMGA0);
t = (0:N-1)/fs;


EMGA0 = bandpass_filter(EMGA0, filter, fs, order);
EMGA1 = bandpass_filter(EMGA1, filter, fs, order);
EMGA2 = bandpass_filter(EMGA2, filter, fs, order);
EMGA3 = bandpass_filter(EMGA3, filter, fs, order);    

%envelop

if do_plot

    subplot(2, 2, 1)
    plot(t, EMGA0);
    title('EMGA0 Data');
    xlabel('Time (s)');
    ylabel('ADC value');
    grid on;
    
    subplot(2, 2, 2)
    % [env1, ~] = envelope(EMGA1, 400*fs, 'rms'); %what value should I take? Is 400 good enough?
    % plot(t, env1);
    plot(t, EMGA1)
    % title('EMGA1 Envelop (RMS)');
    title('EMGA1 Data');
    xlabel('Time (s)');
    ylabel('ADC value');
    grid on;
    
    subplot(2, 2, 3)
    plot(t, EMGA2);
    % ylim([0, 1024]);
    title('EMGA2 Data');
    xlabel('Time (s)');
    ylabel('ADC value');
    grid on;
    
    subplot(2, 2, 4)
    plot(t, EMGA3);
    % ylim([0, 1024]);
    title('EMGA3 Data');
    xlabel('Time (s)');
    ylabel('ADC value');
    grid on;
end