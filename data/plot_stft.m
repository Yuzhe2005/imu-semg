function [t, f, p_db, s] = plot_stft(audioData, fs, windowSize, fileName)

% Define parameters
minFreq = 20;  % Minimum frequency in Hz
maxFreq = 498;  % Maximum frequency in Hz
% windowSize = 2048;  % Window size
windowType = hann(windowSize);  % Hann window
nfft = windowSize * 2;  % Zero-padding factor of 2
overlap = windowSize / 2;  % 50% overlap

% Compute the spectrogram
[s, f, t, p] = spectrogram(audioData, windowType, overlap, nfft, fs);

% Convert to dB scale for visualization
p_db = 10*log10(abs(p));

% Restrict frequency range to minFreq and maxFreq
freqIdx = (f >= minFreq) & (f <= maxFreq);
p_db = p_db(freqIdx, :);
f = f(freqIdx);

% Plot the spectrogram
imagesc(t, f, p_db);
axis xy;
colormap('parula');  % Use a suitable colormap, e.g., parula
colorbar;
xlabel('Time (s)');
ylabel('Frequency (Hz)');

title(['Spectrogram on ', fileName]);
end