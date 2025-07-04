function signal_out = bandpass_filter(signal_in, filter_range, fs, order)
% bandpass_filter - Apply a simple bandpass filter using sequential butterworth filters
%
% Syntax: signal_out = bandpass_filter(signal_in, filter_range, fs)
%
% Inputs:
%    signal_in    - Input 1D signal (vector)
%    filter_range - [low_cutoff, high_cutoff] in Hz
%    fs           - Sampling frequency in Hz
%
% Outputs:
%    signal_out   - Filtered signal (same size as input)
%
% Description:
%    First applies a high-pass Butterworth filter at filter_range(1),
%    then applies a low-pass Butterworth filter at filter_range(2),
%    using zero-phase filtering (filtfilt) to avoid phase distortion.

% order= 24;

% First-stage high-pass filter
fc_high = filter_range(1);
[b_high, a_high] = butter(order, fc_high/(fs/2), 'high');
signal_out = filtfilt(b_high, a_high, signal_in);

% Second-stage low-pass filter
fc_low = filter_range(2);
[b_low, a_low] = butter(order, fc_low/(fs/2), 'low');
signal_out = filtfilt(b_low, a_low, signal_out);

end