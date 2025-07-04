crop_time = [20, 115];
fs = 1300;

muscle_names = {'A0', 'A1', 'A2', 'A3'};
num_muscles = length(muscle_names);

rms_all = cell(num_muscles, 1);  %Root Mean Square
mpf_all = cell(num_muscles, 1);  %Mean Power Frequency
mf_all  = cell(num_muscles, 1);  %Mean Frequency
mdf_all = cell(num_muscles, 1);  %Median Power Frquency

data_path = 'C:\Users\dwang\Desktop\IMU+sEMG\data\testing data\sEMG_data_David_612_A1.mat';

[A0, A1, A2, A3] = plot_MyowareData(data_path, 'crop_range', [5, -1], 'do_plot', true);

A0 = A0(crop_time(1)*fs : crop_time(2)*fs);
A1 = A1(crop_time(1)*fs : crop_time(2)*fs);
A2 = A2(crop_time(1)*fs : crop_time(2)*fs);
A3 = A3(crop_time(1)*fs : crop_time(2)*fs);

sEMG = {A0, A1, A2, A3};

for m = 1 : num_muscles
    ch_filtered   = sEMG{m};
    L             = length(ch_filtered);
    segmentLength = fs;
    numSegments   = floor(L / segmentLength);
    segments      = zeros(numSegments, segmentLength);

    for i = 1:numSegments
        idxStart       = (i-1)*segmentLength + 1;
        idxEnd         = i*segmentLength;
        segments(i, :) = ch_filtered(idxStart:idxEnd);
    end

    rms_t = zeros(numSegments, 1);
    mpf_t = zeros(numSegments, 1);
    mf_t  = zeros(numSegments, 1);
    mdf_t = zeros(numSegments, 1);    % MDF array

    for i = 1:numSegments
        [rms_val, mpf_val, mf_val] = analyzeEpoch(segments(i,:), fs);
        mdf_val = medfreq(segments(i,:), fs);  % Compute Median Power Frequency

        rms_t(i) = rms_val;
        mpf_t(i) = mpf_val;
        mf_t(i)  = mf_val;
        mdf_t(i) = mdf_val;
    end

    rms_all{m} = rms_t;
    mpf_all{m} = mpf_t;
    mf_all{m}  = mf_t;
    mdf_all{m} = mdf_t;
end

figure('Name', 'All Muscles - RMS, MF, MPF and MDF', 'NumberTitle', 'off');
muscle_labels = {'A0', 'A1', 'A2', 'A3'};

for m = 1:num_muscles
    subplot(num_muscles/2, num_muscles/2, m);
    hold on;

    t = (1:length(rms_all{m}));

    plot(t, rms_all{m},  '-', 'LineWidth', 1.2);
    plot(t, mpf_all{m},  '-', 'LineWidth', 1.2);
    plot(t, mf_all{m},   '-', 'LineWidth', 1.2);
    plot(t, mdf_all{m},  '-', 'LineWidth', 1.2);

    % Linear fits and slope annotations
    p_rms = polyfit(t, rms_all{m}, 1);
    plot(t, polyval(p_rms, t), '--', 'LineWidth', 1);
    text(t(end), polyval(p_rms, t(end)), sprintf('%.4f', p_rms(1)), ...
         'HorizontalAlignment','right','VerticalAlignment','bottom');

    p_mpf = polyfit(t, mpf_all{m}, 1);
    plot(t, polyval(p_mpf, t), '--', 'LineWidth', 1);
    text(t(end), polyval(p_mpf, t(end)), sprintf('%.2f', p_mpf(1)), ...
         'HorizontalAlignment','right','VerticalAlignment','bottom');

    p_mf = polyfit(t, mf_all{m}, 1);
    plot(t, polyval(p_mf, t), '--', 'LineWidth', 1);
    text(t(end), polyval(p_mf, t(end)), sprintf('%.2f', p_mf(1)), ...
         'HorizontalAlignment','right','VerticalAlignment','bottom');

    p_mdf = polyfit(t, mdf_all{m}, 1);
    plot(t, polyval(p_mdf, t), '--', 'LineWidth', 1);
    text(t(end), polyval(p_mdf, t(end)), sprintf('%.2f', p_mdf(1)), ...
         'HorizontalAlignment','right','VerticalAlignment','bottom');

    grid on;
    xlabel('Time (s)');
    ylabel(muscle_labels{m});

    legend('RMS','MPF','MF','MDF','RMSL','MPFL','MFL','MDFL', 'Location','eastoutside');
    hold off;
end
