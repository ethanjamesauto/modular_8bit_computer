import serial
import matplotlib.pyplot as plt
import numpy as np
import time


ser = serial.Serial('COM8',9600,timeout=2,bytesize=serial.EIGHTBITS)
time.sleep(2)
NUM_ELEMENTS = 4
VERT_PLOT_OFFSET = 130
RECORD_MODE = int(input("record mode: "))

# Initialize plot
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()
xdata, ydata0,ydata1,ydata2,ydata3 = [], [], [], [], []
line0, = ax.plot([], [], lw=2,color='red')
line1, = ax.plot([], [], lw=2,color='orange')
line2, = ax.plot([], [], lw=2,color='yellow')
line3, = ax.plot([], [], lw=2,color='green')
ax.set_xlim(0, 1000)  # Adjust as needed
ax.set_ylim(0, 530)  # Adjust as needed
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
old_len_samples = 0
if RECORD_MODE == 1:
    try:
        #start_time = time.time()
        while True:
            if ser.in_waiting > 0:
                try:
                    
                    # Read and decode the data
                    data = ser.readline().decode('utf-8').strip().split(" ")
                    
                    if len(data) == NUM_ELEMENTS + 1:
                        ydata0.append(int(data[1]))
                        ydata1.append(int(data[2])+VERT_PLOT_OFFSET)
                        ydata2.append(int(data[3])+2*VERT_PLOT_OFFSET)
                        ydata3.append(int(data[4])+3*VERT_PLOT_OFFSET)
                        xdata.append(int(data[0]))
                        #ydata = []
                        #for i in range( len(data[0])):
                        
                        if len(xdata) > old_len_samples:
                            ax.set_xlim(max(xdata)-10000,max(xdata)+100)  # Adjust as needed
                            #ax.set_ylim(min(ydata)-1,max(ydata)+1)  # Adjust as needed
                        
                        
                            line0.set_data(xdata, ydata0)
                            line1.set_data(xdata, ydata1)
                            line2.set_data(xdata, ydata2)
                            line3.set_data(xdata, ydata3)
                            fig.canvas.draw_idle()
                            fig.canvas.flush_events() 
                            old_len_samples = len(xdata)+10
                        #y = float(data)  # Convert to float (adjust as needed)
                    #xdata.append(int(data))
                    #ydata.append(counter)
                    
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
elif RECORD_MODE == 0:
    #in record mode zero, the arduino is controlling the 8b computer clock.
    counter = -8
    hold = True
    while hold:
        #try:
        if ser.in_waiting > 1:
            data = ser.readline().decode('utf-8').strip().split(" ")
            if data == ['10']:
                print("connected to weeno")
                while True:
                    var = "mode"
                    ser.write(var.encode())
                    #print("waiting response")
            #hold = False
        #except:
            #print("guh")
            #time.sleep(0.5)
        
            #pass
    try:
        #start_time = time.time()
        while True:
            if ser.in_waiting > 15:
                try:
                    data = ser.readline().decode('utf-8').strip().split(" ")
                    if len(data) == NUM_ELEMENTS + 1:
                        trigger_time = data[0]
                        ydata0.append(int(data[1]))
                        ydata1.append(int(data[2])+VERT_PLOT_OFFSET)
                        ydata2.append(int(data[3])+2*VERT_PLOT_OFFSET)
                        ydata3.append(int(data[4])+3*VERT_PLOT_OFFSET)
                        xdata = range(0,16)
                        counter = counter + 1
                        #ydata = []
                        #for i in range( len(data[0])):
                        
                        if len(xdata) == 16:
                            ax.set_xlim(0,16)  # Adjust as needed
                            #ax.set_ylim(min(ydata)-1,max(ydata)+1)  # Adjust as needed
                        
                        
                            line0.set_data(xdata, ydata0)
                            line1.set_data(xdata, ydata1)
                            line2.set_data(xdata, ydata2)
                            line3.set_data(xdata, ydata3)
                            fig.canvas.draw_idle()
                            fig.canvas.flush_events() 
                            old_len_samples = len(xdata)+10
                            xdata = []
                            ydata0 = []
                            ydata1 = []
                            ydata2 = []
                            ydata3 = []
                            counter = -8

                except ValueError:
                    pass  # Handle the case where data is not a valid float
            #  

    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        # Close the serial connection when done
        ser.close()