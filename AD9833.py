import serial, cv2 as cv, numpy as np, time

esp = serial.Serial(baudrate = 250000, port = "COM3")
esp.set_buffer_size(1900)

try:
    while True:
        data = esp.read(1900);
        data = list(data);
        mult = 5; data = [j*mult for j in data];
        sc = np.full((400,1900,3), 255, 'uint8');
        
        for i in range(1900):
            sc[data[i]:data[i]+3, i, (0,1)] = 0;

        cv.imshow('B-)', sc); cv.moveWindow('B-)', 0, 0);
        cv.waitKey(1)
        

except:
    esp.close()
    cv.destroyAllWindows()
