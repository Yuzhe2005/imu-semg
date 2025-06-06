function[rms0_env, rms1_env, rms2_env, rms3_env] = calculate_RMS(data_path, window_ms, varargin)
%   calculate_RMS('myData.mat', 200);             
%   calculate_RMS('myData.mat', 100, 'crop_range',[10,-5]);

    fs = 1300;

    [EMGA0, EMGA1, EMGA2, EMGA3] = plot_MyowareData(data_path, varargin{:});

    if ~(isscalar(window_ms) && window_ms > 0)
        error('calculate_RMS:BadWindow', 'window_ms must be positive');
    end

    window_size = round(window_ms * fs / 1000);
    if window_size < 1
        window_size = 1;
    end

    rms0_env = sqrt(movmean(EMGA0.^2, window_size));
    rms1_env = sqrt(movmean(EMGA1.^2, window_size));
    rms2_env = sqrt(movmean(EMGA2.^2, window_size));
    rms3_env = sqrt(movmean(EMGA3.^2, window_size));

    N = length(rms0_env);
    t = (0:(N-1)) / fs;  

    figure;
    subplot(2,2,1)
    plot(t, rms0_env);
    title(sprintf('Channel A0 RMS (window = %d ms)', window_ms));
    xlabel('Time (s)');
    ylabel('RMS');
    grid on

    subplot(2,2,2)
    plot(t, rms1_env);
    title(sprintf('Channel A1 RMS (window = %d ms)', window_ms));
    xlabel('Time (s)');
    ylabel('RMS');
    grid on

    subplot(2,2,3)
    plot(t, rms2_env);
    title(sprintf('Channel A2 RMS (window = %d ms)', window_ms));
    xlabel('Time (s)');
    ylabel('RMS');
    grid on

    subplot(2,2,4)
    plot(t, rms3_env);
    title(sprintf('Channel A3 RMS (window = %d ms)', window_ms));
    xlabel('Time (s)');
    ylabel('RMS');
    grid on
end
