function plot_AdafruitData(data_path, varargin)
    crop_range = [5, -1];
    for i = 1:2:length(varargin)
        if strcmp(varargin{i}, 'crop_range')
            crop_range = varargin{i+1};
        end
    end

    S = load(data_path);
    try
        % IMUax = detrend(S.ax);
        % IMUay = detrend(S.ay);
        % IMUaz = detrend(S.az);    
        % IMUgx = detrend(S.gx);
        % IMUgy = detrend(S.gy);
        % IMUgz = detrend(S.gz);
        IMUax = (S.ax);
        IMUay = (S.ay);
        IMUaz = (S.az);    
        IMUgx = (S.gx);
        IMUgy = (S.gy);
        IMUgz = (S.gz);
    catch
        warning("Couldn't find one of ax, ay, az, gx, gy, gz in %s", data_path);
        return
    end

    idx = crop_range(1) : (length(IMUax) + crop_range(2));
    IMUax = IMUax(idx);
    IMUay = IMUay(idx);
    IMUaz = IMUaz(idx);
    IMUgx = IMUgx(idx);
    IMUgy = IMUgy(idx);
    IMUgz = IMUgz(idx);

    % force columns (so [true; …] concatenates correctly)
    IMUax = IMUax(:);
    IMUay = IMUay(:);
    IMUaz = IMUaz(:);
    IMUgx = IMUgx(:);
    IMUgy = IMUgy(:);
    IMUgz = IMUgz(:);

    % remove consecutive repeats of any length
    IMUax = IMUax([ true; diff(IMUax) ~= 0 ]);
    IMUay = IMUay([ true; diff(IMUay) ~= 0 ]);
    IMUaz = IMUaz([ true; diff(IMUaz) ~= 0 ]);
    IMUgx = IMUgx([ true; diff(IMUgx) ~= 0 ]);
    IMUgy = IMUgy([ true; diff(IMUgy) ~= 0 ]);
    IMUgz = IMUgz([ true; diff(IMUgz) ~= 0 ]);

    % ---- plotting ----
    figure;

    subplot(3,2,1)
    plot(IMUax);
    title('Accelerometer X-axis');
    xlabel('Samples');
    ylabel('Acceleration (m/s^2)');
    grid on;

    subplot(3,2,2)
    plot(IMUay);
    title('Accelerometer Y-axis');
    xlabel('Samples');
    ylabel('Acceleration (m/s^2)');
    grid on;

    subplot(3,2,3)
    plot(IMUaz);
    title('Accelerometer Z-axis');
    xlabel('Samples');
    ylabel('Acceleration (m/s^2)');
    grid on;

    subplot(3,2,4)
    plot(IMUgx);
    title('Gyroscope X-axis');
    xlabel('Samples');
    ylabel('Angular Velocity (rad/s)');
    grid on;

    subplot(3,2,5)
    plot(IMUgy);
    title('Gyroscope Y-axis');
    xlabel('Samples');
    ylabel('Angular Velocity (rad/s)');
    grid on;

    subplot(3,2,6)
    plot(IMUgz);
    title('Gyroscope Z-axis');
    xlabel('Samples');
    ylabel('Angular Velocity (rad/s)');
    grid on;
end
