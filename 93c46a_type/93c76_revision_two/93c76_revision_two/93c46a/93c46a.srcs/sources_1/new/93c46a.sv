// module author Henry Pritchard
// 11.3.2024
// from 93c46a datasheet
// https://ww1.microchip.com/downloads/aemDocuments/documents/MPD/ProductDocuments/DataSheets/93AA46A-B-C-93LC46A-B-C-93C46A-B-C-1-Kbit-Microwire-Compatible-Serial-EEPROM-Data-Sheet-DS20001749.pdf

module test_93c46a(
    input cs,
    input clk,
    input din,
    output dout);
    
    typedef enum logic [1:0]{RESET, COMMAND_CODE, ADDRESS, DATA_OUT} state_machine;
    
    state_machine state;
    logic [0] cs_n;
    assign cs_n = ~cs;
    int command_code_index = 0;
    logic [5:0] specified_address = 6'b000000;
    
    always@(posedge clk or posedge cs_n)begin
        if(cs)begin //state machine is only active while chip selected. if cs drops low, state machine resets to reset state
            case (state)
                RESET:
                    //exiting reset state if cs and di are both high w.r.t. posedge clock (pg 7 datasheet)
                    if(din)begin
                        state <= COMMAND_CODE; // first bit indicates that the chip is being activated and the command code is being entered.
                        command_code_index = 0;
                    end
                COMMAND_CODE:
                    // for now I will only implement the read code. 
                    if (din) begin
                        if(command_code_index == 0)begin
                            //first bit in read code is a one.
                            state <= COMMAND_CODE;
                            command_code_index = command_code_index + 1;
                        end
                    end else begin
                        if(command_code_index == 1)begin
                            state <= ADDRESS; //read code is entered. now 
                            command_code_index = 6; //first index is 5, drops down to 0
                        end else begin
                            state <= RESET; // invalid code entered.
                            command_code_index = 0;
                        end
                        
                    end
                ADDRESS:
                    specified_address[command_code_index] = din;
                    if(command_code_index == 0)begin
                        state <= DATA_OUT;
                    end
                DATA_OUT:
        end else begin
            state <= RESET;
        end
    end
    
endmodule
   