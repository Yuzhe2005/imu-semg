function [freqs, amplitude] = plotFFT(data, fs)
% plotFFT  Compute and plot the single-sided FFT amplitude spectrum.
%
%   [freqs, amplitude] = plotFFT(data, fs)
%
%   Inputs:
%     data  - 1×n or n×1 real signal vector
%     fs    - sampling frequency in Hz (scalar). If omitted, defaults to 1.
%
%   Outputs:
%     freqs     - frequency bins (0 to Nyquist) in Hz
%     amplitude - single-sided amplitude spectrum

    if nargin < 2 || isempty(fs)
        fs = 1300;
    end
    % If the user didn't supply a sampling rate (fs), or passed in []
    % then default fs to 1 Hz so the code still runs.

    x = data(:).';        
    % Convert any shape of vector into a row vector:
    %   data(:) makes it a column, then .' transposes to 1×n.

    n = numel(x);
    % Count the number of samples in x (the length of the vector).

    Y = fft(x);
    % Compute the discrete Fourier transform of the signal x.

    P2 = abs(Y) / n;                          
    % Take magnitude of the complex FFT result and normalize by n.
    % This gives the two-sided amplitude spectrum.

    P1 = P2(1:floor(n/2)+1);                 
    % Extract the first half of the spectrum (from DC up to Nyquist).
    % floor(n/2)+1 handles both even and odd n correctly.

    P1(2:end-1) = 2 * P1(2:end-1);           
    % Double all amplitudes except the endpoints (DC and Nyquist)
    % to account for the energy in the discarded second half.

    freqs = fs * (0:floor(n/2)) / n;
    % Build the frequency axis in Hz:
    %   (0:floor(n/2)) are the bin indices,
    %   multiplied by fs/n gives frequency per bin.

    figure;
    % Open a new figure window for the plot.

    plot(freqs, P1, 'LineWidth', 1.2);
    % Plot frequency vs. amplitude with a slightly thicker line.

    grid on;
    % Turn on the grid to make it easier to read values.

    xlabel('Frequency (Hz)');
    % Label the x-axis.

    ylabel('Amplitude');
    % Label the y-axis.

    title('Single-Sided Amplitude Spectrum');
    % Add a title describing the plot.

    amplitude = P1;
    % Return the single-sided amplitude spectrum to the caller.

end
