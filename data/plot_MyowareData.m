function [EMGA0, EMGA1, EMGA2, EMGA3] = plot_MyowareData(data_path, varargin)
crop_range = [5, -1];
for i = 1:2:length(varargin)
    if strcmp(varargin{i}, 'crop_range')
        crop_range = varargin{i+1};
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

subplot(2, 2, 1)
plot(EMGA0);
title('EMGA0 Data');
xlabel('Samples');
ylabel('ADC value');
grid on;

subplot(2, 2, 2)
plot(EMGA1);
title('EMGA1 Data');
xlabel('Samples');
ylabel('ADC value');
grid on;

subplot(2, 2, 3)
plot(EMGA2);
title('EMGA2 Data');
xlabel('Samples');
ylabel('ADC value');
grid on;

subplot(2, 2, 4)
plot(EMGA3);
title('EMGA3 Data');
xlabel('Samples');
ylabel('ADC value');
grid on;