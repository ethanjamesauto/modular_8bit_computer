import serial
import matplotlib.pyplot as plt
import numpy as np
import time


ser = serial.Serial('COM8',9600,timeout=1,bytesize=serial.EIGHTBITS)


# Initialize plot
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()
xdata, ydata = [], []
line, = ax.plot([], [], lw=2)
ax.set_xlim(0, 16)  # Adjust as needed
ax.set_ylim(0, 300)  # Adjust as needed
ax.set_xlabel('Sample')
ax.set_ylabel('Value')
ax.set_title('Live Data Plot')

# This function will be used to update the data without redrawing the plot
# def update_plot(xdata, ydata):
#     line.set_data(xdata, ydata)
#     # Adjust x-axis limits to keep the most recent 100 points visible
#     if len(xdata) > 100:
#         ax.set_xlim(xdata[-100], xdata[-1])
#     # Only update the plot if data has changed
#     fig.canvas.draw_idle()
#     fig.canvas.flush_events()

try:
    start_time = time.time()
    while True:
        counter = 0
        if ser.in_waiting > 0:
            try:
                # Read and decode the data
                data = ser.readline().decode('utf-8').strip().split(" ")
                ydata = []
                for i in range( len(data)):
                    ydata.append(int(data[i]))
                xdata = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
                ax.set_xlim(min(xdata)-1,max(xdata)+1)  # Adjust as needed
                ax.set_ylim(min(ydata)-1,max(ydata)+1)  # Adjust as needed
                
                
                line.set_data(xdata, ydata)
                #y = float(data)  # Convert to float (adjust as needed)
                #xdata.append(int(data))
                #ydata.append(counter)
                fig.canvas.draw_idle()
                fig.canvas.flush_events()  
                # Append new data to lists
                #current_time = time.time() - start_time
                #
                #ydata.append(y)
                
                # Update plot
                #update_plot(xdata, ydata)
                
            except ValueError:
                pass  # Handle the case where data is not a valid float
        #  
        #print(xdata,ydata)
        #fig.canvas.draw_idle()
        #fig.canvas.flush_events()      
        #xdata, ydata = [], []
        #time.sleep(0.1)  # Adjust the sleep time as needed

except KeyboardInterrupt:
    print("Interrupted by user.")

finally:
    # Close the serial connection when done
    ser.close()
    #plt.ioff()  # Turn off interactive mode
    #plt.show()