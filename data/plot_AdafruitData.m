function plot_AdafruitData(data_path, varargin)
crop_range = [5, -1];
for i = 1:2:length(varargin)
    if strcmp(varargin{i}, 'crop_range')
        crop_range = varargin{i+1};
    end
end

S = load(data_path);
try
    IMUax = detrend(S.ax);
    % IMUax = S.ax;
    IMUay = detrend(S.ay);
    IMUaz = detrend(S.ax);
    IMUgx = detrend(S.gx);
    IMUgy = detrend(S.gy);
    IMUgz = detrend(S.gz);
catch 
    disp("Didn't find the sensor data")
    return
end

IMUax = IMUax(crop_range(1):end+crop_range(2));
IMUay = IMUay(crop_range(1):end+crop_range(2));
IMUaz = IMUaz(crop_range(1):end+crop_range(2));
IMUgx = IMUgx(crop_range(1):end+crop_range(2));
IMUgy = IMUgy(crop_range(1):end+crop_range(2));
IMUgz = IMUgz(crop_range(1):end+crop_range(2));

subplot(3, 2, 1)
plot(IMUax);
title('Accelerometer X-axis');
xlabel('Samples');
ylabel('Acceleration (m/s^2)');
grid on;

subplot(3, 2, 2)
plot(IMUay);
title('Accelerometer Y-axis');
xlabel('Samples');
ylabel('Acceleration (m/s^2)');
grid on;

subplot(3, 2, 3)
plot(IMUaz);
title('Accelerometer Z-axis');
xlabel('Samples');
ylabel('Acceleration (m/s^2)');
grid on;

subplot(3, 2, 4)
plot(IMUgx);
title('Gyroscope X-axis');
xlabel('Samples');
ylabel('Angular Velocity (rad/s)');
grid on;

subplot(3, 2, 5)
plot(IMUgy);
title('Gyroscope Y-axis');
xlabel('Samples');
ylabel('Angular Velocity (rad/s)');
grid on;

subplot(3, 2, 6)
plot(IMUgz);
title('Gyroscope Z-axis');
xlabel('Samples');
ylabel('Angular Velocity (rad/s)');
grid on;


