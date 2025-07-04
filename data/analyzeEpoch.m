function [rms_val, mpf_val, mf_val] = analyzeEpoch(x_epoch, fs)
    % x_epoch: 1D array of samples for the epoch
    % fs: sampling rate in Hz

    N = length(x_epoch);

    % 1) Time-Domain RMS
    rms_val = sqrt(mean(x_epoch.^2));

    % 2) Compute one-sided Power Spectrum
    % x_epoch = reshape(x_epoch,[1,N]);
    % w = hamming(N);
    % Y = fft(x_epoch'.*w);
    % % Y = fft(x_epoch);
    % P2 = abs(Y / N).^2;       % two-sided power
    % P1 = P2(1:(N/2+1));       % one-sided
    % P1(2:end-1) = 2 * P1(2:end-1);
    % 
    % % Frequency axis (one-sided)
    % f = (0:(N/2))*(fs/N);
    % frange = (f>5) & (f<1000);
    % P = P1(frange);
    [P1, P, f, frange, peakInHz, peakIndex] = plot_powerSpectrum(x_epoch, fs);
    f = f(frange);
    f=f(:);
    P=P(:);
    % 3) Mean Power Frequency (MPF)
    total_power = sum(P);
    weighted_sum = sum(f .* P);
    mpf_val = weighted_sum / total_power;

    % 4) Median Frequency (MF)
    cumsum_power = cumsum(P);
    half_power = 0.5 * total_power;
    idx_median = find(cumsum_power >= half_power, 1, 'first');
    mf_val = f(idx_median);
end