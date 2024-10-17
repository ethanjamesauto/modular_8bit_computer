import serial
import matplotlib.pyplot as plt
import numpy as np
import time


ser = serial.Serial('COM8',9600,timeout=2,bytesize=serial.EIGHTBITS)
time.sleep(2)
NUM_ELEMENTS = 7
VERT_PLOT_OFFSET = 300
RECORD_MODE = 1#int(input("record mode: "))

# Initialize plot
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()
xdata, ydata0,ydata1,ydata2,ydata3,ydata4,ydata5,ydata6 = [], [], [], [], [], [], [], []
line0, = ax.plot([], [], lw=2,color='red')
line1, = ax.plot([], [], lw=2,color='orange')
line2, = ax.plot([], [], lw=2,color='yellow')
line3, = ax.plot([], [], lw=2,color='green')
line4, = ax.plot([], [], lw=2,color='blue')
line5, = ax.plot([], [], lw=2,color='purple')
line6, = ax.plot([], [], lw=2,color='gray')
ax.set_xlim(0, 1000)  # Adjust as needed
ax.set_ylim(0, 2500)  # Adjust as needed
ax.set_xlabel('Sample')
ax.set_ylabel('Value')
ax.set_title('Live Data Plot')

WRITEBACK_FILENAME = "recording.txt"
CHANNEL_NAMES = ["timestamp","address lower","address upper","data bus","pc lower","pc upper","internal bus","instruction"]

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
clock_counter = 0
old_data = []
detected_reset = False
if RECORD_MODE == 1:
    with open(WRITEBACK_FILENAME,"w") as fp:
        try:
            #start_time = time.time()
            while True:
                if ser.in_waiting > 0:
                    try:
                        
                        # Read and decode the data
                        data = ser.readline().decode('utf-8').strip().split(" ")
                        if len(old_data) > 0:
                           if data[0] < old_data[0]:
                               detected_reset = True
                                
                        #if the packet includes new values:
                        #print(data[1:],data[1:])
                        equal_data = True
                        if len(data) == len(old_data):
                            for index_data in range(len(data)-1):
                                if equal_data:
                                    if(data[index_data+1] != old_data[index_data+1]):
                                        equal_data = False
                        else:
                            equal_data = False
                        print(equal_data)

                        if not equal_data:
                            if not detected_reset:

                                fp.write("-----------"+str(clock_counter)+"---------\n")
                                index = 0
                                for item in data:
                                    if index < len(CHANNEL_NAMES):
                                        fp.write(CHANNEL_NAMES[index] + " : " + str(data[index])+"\n")

                                    index = index + 1
                                fp.write("\n")
                                fp.write("\n")
                                clock_counter = clock_counter + 1
                                old_data = data
                            # else:
                            #     if int(old_data[0]) - int(data[0]) > 10:
                            #         print("DETECTED RESET")

                            #         #if len(data) > 1:
                            #         xdata, ydata0,ydata1,ydata2,ydata3,ydata4,ydata5,ydata6 = [], [], [], [], [], [], [], []
                            #             #detected_reset = True
                            #         fig, ax = plt.subplots()
                            #         ax.set_xlim(0, 1000)  # Adjust as needed
                            #         ax.set_ylim(0, 2500)  # Adjust as needed
                            #         fig.canvas.draw_idle()
                            #         fig.canvas.flush_events()
                            #         detected_reset = False
                            #         continue
                        else:
                            old_data = data


                        
                        if len(data) == NUM_ELEMENTS + 1:
                            ydata0.append((int(data[1])))
                            ydata1.append((int(data[2])+VERT_PLOT_OFFSET))
                            ydata2.append((int(data[3])+2*VERT_PLOT_OFFSET))
                            ydata3.append((int(data[4])+3*VERT_PLOT_OFFSET))
                            ydata4.append((int(data[5])+4*VERT_PLOT_OFFSET))
                            ydata5.append((int(data[6])+5*VERT_PLOT_OFFSET))
                            ydata6.append((int(data[7])+6*VERT_PLOT_OFFSET))
                            xdata.append(int(data[0]))
                            #ydata = []
                            #for i in range( len(data[0])):
                            
                            if len(xdata) > old_len_samples:

                                



                                ax.set_xlim(max(xdata)-10000,max(xdata)+100)  # Adjust as needed
                                #ax.set_ylim(min(ydata)-1,max(ydata)+1)  # Adjust as needed
                            
                            
                                line0.set_data(xdata, ydata0)
                                #for i, j in zip(xdata, ydata0):
                                plt.text(xdata[len(xdata)-1], ydata0[len(ydata0)-1], str(data[1]), ha='center', va='bottom')
                                line1.set_data(xdata, ydata1)
                                plt.text(xdata[len(xdata)-1], ydata1[len(ydata1)-1], str(data[2]), ha='center', va='bottom')
                                line2.set_data(xdata, ydata2)
                                plt.text(xdata[len(xdata)-1], ydata2[len(ydata2)-1], str(data[3]), ha='center', va='bottom')
                                line3.set_data(xdata, ydata3)
                                plt.text(xdata[len(xdata)-1], ydata3[len(ydata3)-1], str(data[4]), ha='center', va='bottom')
                                line4.set_data(xdata, ydata4)
                                plt.text(xdata[len(xdata)-1], ydata4[len(ydata4)-1], str(data[5]), ha='center', va='bottom')
                                line5.set_data(xdata, ydata5)
                                plt.text(xdata[len(xdata)-1], ydata5[len(ydata5)-1], str(data[6]), ha='center', va='bottom')
                                line6.set_data(xdata, ydata6)
                                plt.text(xdata[len(xdata)-1], ydata6[len(ydata6)-1], str(data[7]), ha='center', va='bottom')
                                fig.canvas.draw_idle()
                                fig.canvas.flush_events() 
                                old_len_samples = len(xdata)+20
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