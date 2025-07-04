function [t, MPF, MF] = plotMPF_MF(filteredEmg, fs, windowSize)
% plotMPF_MF   Compute & plot the Mean and Median Frequency of sEMG over time
%
%   [t, MPF, MF] = plotMPF_MF(filteredEmg, fs, windowSize)
%
%   Inputs:
%     filteredEmg - n×1 or 1×n vector of your already filtered EMG signal
%     fs          - sampling frequency in Hz (e.g. 1300)
%     windowSize  - STFT window length in samples (e.g. 2048)
%
%   Outputs:
%     t   - 1×numFrames time‐axis for each STFT slice (s)
%     MPF - 1×numFrames Mean Power Frequency (Hz)
%     MF  - 1×numFrames Median Frequency (Hz)

    % ensure row vector
    x = filteredEmg(:).';
    n = numel(x);

    % STFT parameters
    w       = hann(windowSize);     % Hann window
    nover   = windowSize/2;         % 50% overlap
    nfft    = windowSize * 2;       % zero‐pad for finer Δf

    % compute STFT (p is power spectral density)
    [~, f, t, p] = spectrogram(x, w, nover, nfft, fs);

    % keep only positive‐frequency power
    P = abs(p);  % linear power

    % optionally restrict to your band (20–498 Hz)
    minF = 20;
    maxF = min(498, fs/2);
    freqMask = (f >= minF) & (f <= maxF);
    f = f(freqMask);
    P = P(freqMask,:);

    % preallocate
    numFrames = size(P,2);
    MPF = zeros(1, numFrames);
    MF  = zeros(1, numFrames);

    % total power per frame
    totalP = sum(P,1);

    for k = 1:numFrames
        Pk = P(:,k);

        % Mean Power Frequency
        MPF(k) = sum(f .* Pk) / totalP(k);

        % Median Frequency: find f where cumulative power = half
        cumP = cumsum(Pk);
        half = totalP(k)/2;
        idx  = find(cumP >= half, 1, 'first');
        MF(k) = f(idx);
    end

    % --- Plotting ---
    figure;
    subplot(2,1,1);
    plot(t, MPF, 'LineWidth', 1.2);
    grid on;
    xlabel('Time (s)');
    ylabel('MPF (Hz)');
    title('Mean Power Frequency over Time');

    subplot(2,1,2);
    plot(t, MF, 'LineWidth', 1.2);
    grid on;
    xlabel('Time (s)');
    ylabel('MF (Hz)');
    title('Median Frequency over Time');
end
