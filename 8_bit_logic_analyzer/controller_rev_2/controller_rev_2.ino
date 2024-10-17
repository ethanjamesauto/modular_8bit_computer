//int triggered  = 5;
//int s_read  = 4;
//int s_write     = 3;
//int s_clk  = 0;
//int s_cs  = 2;
//int da_clear = 12;

int s_clk = 7;
int p_load = 5;
int cpu_clock = 6;
int w_enable = 8;
int addr_0 = 9;
int addr_1 = 10;
int addr_2 = 11;
int addr_3 = 12;
int s_in = 4;
int cpu_reset_n = 3;
int trigger_clear = 2;
int trigger = 13;

int RECORD_MODE = 1; // mode one is recording as close to real time as possible.
int NUM_ELEMENTS_IN_CHAIN = 7;
int RAM_SIZE = 16;

//void spi_write(byte to_send){
//  for(int i = 0; i < 8; i++){
//    digitalWrite(s_out,bitRead(to_send,i));
//    digitalWrite(s_clk,true);
//    digitalWrite(s_clk,false);
//  }
//  digitalWrite(s_out,LOW);
//}

byte spi_read(){
  uint8_t  to_read = 0;
  for(int i = 0;i < 8;i++){
    
    to_read |= (!digitalRead(s_in) << i);
    digitalWrite(s_clk,true);
    
    digitalWrite(s_clk,false);
  }
//  for(int i = 4;i < 8;i++){
//    to_read |= 0 << i;
//  }
  return to_read;
}


void set_address(int number) {
    if (number < 0 || number > 15) {
        Serial.print("Error: Number must be between 0 and 15. ");
        Serial.println(number);
        return;
    }
    digitalWrite(addr_0, (number & 0b0001) ? HIGH : LOW); // Bit 0
    digitalWrite(addr_1, (number & 0b0010) ? HIGH : LOW); // Bit 1
    digitalWrite(addr_2, (number & 0b0100) ? HIGH : LOW); // Bit 2
    digitalWrite(addr_3, (number & 0b1000) ? HIGH : LOW); // Bit 3
}

uint8_t* read_all_from_ram(){
  for(int i = 0; i < RAM_SIZE; i++){

    set_address(i);
    //latch from 189's
    digitalWrite(p_load, LOW);
    digitalWrite(s_clk, HIGH);
    digitalWrite(s_clk,LOW);
    digitalWrite(p_load, HIGH);
    Serial.print(millis());
    Serial.print(" ");
    for(int k = 0; k < NUM_ELEMENTS_IN_CHAIN; k++){
      uint8_t data = spi_read();
//      for (int j = 7; j >= 0; j--) {
//          Serial.print((data >> j) & 1); // Print each bit from highest to lowest
//      }
//      Serial.print(" ");


      //print to serial the ints of what was read
      Serial.print(data);
      Serial.print(" ");
      
    }
    
    Serial.println("");
  }
}

void collect_data(int increment){
  
  for(int i = 0; i < RAM_SIZE; i++){
    //TODO REVISIT this . stepping to next addr may violate setup time required to latch the value written.
    set_address(i);
    digitalWrite(w_enable, LOW);
    delay(increment);//record for the entire sample time. actual value is 
    digitalWrite(w_enable, HIGH);
    
  }
  digitalWrite(w_enable, HIGH);
}


//String byte_to_string(byte toString){
//  String returnString;
//  for(int i = 0;i < 4;i++){
//    char c[1];
//    returnString = returnString + itoa(bitRead(toString,i),c,10);
//  }
//  return returnString;
//}



void setup(){
  pinMode(s_clk, OUTPUT);
  pinMode(p_load, OUTPUT);
  pinMode(cpu_clock, OUTPUT);
  pinMode(w_enable, OUTPUT);
  pinMode(addr_0, OUTPUT);
  pinMode(addr_1, OUTPUT);
  pinMode(addr_2, OUTPUT);
  pinMode(addr_3, OUTPUT);
  pinMode(cpu_reset_n, OUTPUT);
  pinMode(s_in, INPUT);
  pinMode(trigger, INPUT);
  pinMode(trigger_clear, OUTPUT);
  Serial.begin(9600);


  
  
  //set to reset conditions
  digitalWrite(s_clk, LOW);
  digitalWrite(cpu_reset_n, LOW); //reset cpu during setup.
  digitalWrite(cpu_reset_n, HIGH);
  digitalWrite(w_enable, HIGH);
  digitalWrite(addr_0, LOW);
  digitalWrite(addr_1, LOW);
  digitalWrite(addr_2, LOW);
  digitalWrite(addr_3, LOW);
  digitalWrite(cpu_clock, LOW);
  digitalWrite(trigger_clear,HIGH);
  //Serial.println(" ");
  //spi_write(0b00001010);
  //spi_write(0b00001111);
//  for(int k = 0; k < NUM_ELEMENTS_IN_CHAIN; k++){
//      uint8_t data = spi_read();
//      for (int j = 7; j >= 0; j--) {
//          Serial.print((data >> j) & 1); // Print each bit from highest to lowest
//      }
//      Serial.print(" ");
//  }
  //Serial.println(" ");
  //Serial.println("Begin Test");

  


  //parameter is how many milliseconds between samples
  //collect_data(10);

  //while(!Serial){
  //  
  //}
  
  
  //Serial.println("End Test");
  
  //SNAG HERE. WAIT FOR CONTEXT COMMAND FROM LAPTOP
  //int incomingByte = 0;
  //uint8_t handshake = 127;
  //while (Serial.available() <= 0){
  //  Serial.println(0b00001010);
  //  delay(300);
  //}
  //incomingByte = Serial.read();
  
  
      
      
      
 
  
  
}

//void setup() {
//    pinMode(triggered, INPUT);
//    pinMode(s_read, INPUT);
//    pinMode(s_write, OUTPUT);
//    pinMode(s_clk, OUTPUT);
//    pinMode(s_cs, OUTPUT);
//    pinMode(da_clear, OUTPUT);
//    Serial.begin(9600);
//    Serial.println("Begin Test");
//
//    //disable the execution of commands:
//    digitalWrite(s_cs, HIGH);
//    digitalWrite(s_write, LOW);
//    digitalWrite(s_clk,LOW);
//    digitalWrite(da_clear,LOW);
//    digitalWrite(da_clear,HIGH);
//
//    spi_write(0b00001110);
//    //spi_write(test_byte);
//    for(int i = 0;i<4;i++){
//      //Serial.println(!digitalRead(s_read));
//      digitalWrite(s_clk,HIGH);
//      delay(1);
//      digitalWrite(s_clk,LOW);
//      delay(1);
//    }
//    
//
//
//}

//

void loop(){
  
  if (RECORD_MODE == 1){ //real time sample
    collect_data(0);
    read_all_from_ram();
    digitalWrite(cpu_clock,HIGH);
    digitalWrite(cpu_clock,LOW);
  }else if(RECORD_MODE == 0){//trigger
    int current_addr = 0;
    digitalWrite(w_enable, HIGH);


    //need to add a d-latch for the trigger
    while(digitalRead(trigger)==false){
      digitalWrite(trigger_clear,HIGH);
      if(current_addr > 15){
        current_addr = 0;
      }
      //set address to new address:
      digitalWrite(addr_0, (current_addr & 0b0001) ? HIGH : LOW); // Bit 0
      digitalWrite(addr_1, (current_addr & 0b0010) ? HIGH : LOW); // Bit 1
      digitalWrite(addr_2, (current_addr & 0b0100) ? HIGH : LOW); // Bit 2
      digitalWrite(addr_3, (current_addr & 0b1000) ? HIGH : LOW); // Bit 3
      digitalWrite(w_enable, LOW);
      delay(1);
      digitalWrite(w_enable, HIGH);
      current_addr = current_addr + 1;
      //clock new val into 
    }
    //triggered. write eight more values immediately after trigger
    int triggered_address = current_addr;
    int trigger_time = millis();
    for(int extras = 0; extras < 8; extras++){
      digitalWrite(addr_0, (current_addr & 0b0001) ? HIGH : LOW); // Bit 0
      digitalWrite(addr_1, (current_addr & 0b0010) ? HIGH : LOW); // Bit 1
      digitalWrite(addr_2, (current_addr & 0b0100) ? HIGH : LOW); // Bit 2
      digitalWrite(addr_3, (current_addr & 0b1000) ? HIGH : LOW); // Bit 3
      digitalWrite(w_enable, LOW);
      delay(1);
      digitalWrite(w_enable, HIGH);
      current_addr = current_addr + 1;
    }
    //asap stop writing when triggered, now triggered
    
    digitalWrite(w_enable, HIGH);


    for(int i = 0; i < 15; i++){
      if(triggered_address + i > 15){
        set_address(triggered_address+i-16);
      }else{
        set_address(triggered_address+ i);
      }
      digitalWrite(p_load, LOW);
      digitalWrite(s_clk, HIGH);
      delay(1);
      digitalWrite(s_clk,LOW);
      digitalWrite(p_load, HIGH);
      Serial.print(trigger_time);
      Serial.print(" ");
      for(int k = 0; k < NUM_ELEMENTS_IN_CHAIN; k++){
        uint8_t data = spi_read();

  
        Serial.print(data);
        Serial.print(" ");
      }
      Serial.println(" ");
      
      
    }
    current_addr = 0;
    digitalWrite(trigger_clear, LOW);
    
    

    
//      set_address(i);
//      //latch from 189's
//      digitalWrite(p_load, LOW);
//      digitalWrite(s_clk, HIGH);
//      digitalWrite(s_clk,LOW);
//      digitalWrite(p_load, HIGH);
//      Serial.print(millis());
//      Serial.print(" ");
//      for(int k = 0; k < NUM_ELEMENTS_IN_CHAIN; k++){
//        uint8_t data = spi_read();
//  //      for (int j = 7; j >= 0; j--) {
//  //          Serial.print((data >> j) & 1); // Print each bit from highest to lowest
//  //      }
//  //      Serial.print(" ");
//  
//      }
//      //print to serial the ints of what was read
//      Serial.print(data);
//      Serial.print(" ");
//      
//    }
//    
//    Serial.println("");
  }
  
}


//void loop() {
//    //send clear command
//    digitalWrite(da_clear,LOW);
//    delay(1);
//    digitalWrite(da_clear,HIGH);
//    delay(1);
//
//    //clear command register
//    spi_write(0b00000000);
//
//
//    //wait for trigger
//    bool not_triggered = true;
//    while (not_triggered == true){
//      not_triggered = digitalRead(triggered);
//      delay(1);
//      //Serial.println("waiting for trigger");
//    }
//
//    byte sample_buffer[16];
//
//    //once trigger has been seen, read first value from buffer then halt.
//    //at this point, the command register is still 0000 (lsb) and the least sig half buffer 189 is selected.
//    //Serial.println("TRIGGERED. READING BUFFER:");
//    for(int buffer_index = 0; buffer_index < 16; buffer_index++){
//      byte sample = 0b00000000;
//   
//    
//      //clock a value from the RAM
//      digitalWrite(s_cs,LOW);
//      digitalWrite(s_clk,HIGH);
//      delay(0.5);
//      digitalWrite(s_cs,HIGH);
//      digitalWrite(s_clk,LOW);
//      delay(0.5);
//
//      //read the value received
//      for(int i = 4;i<8;i++){
//        sample |= digitalRead(s_read) << i;
//        digitalWrite(s_clk, HIGH);
//        delay(0.5);
//        digitalWrite(s_clk, LOW);
//        delay(0.5);
//      }
//
//      //disable the least sig half 189 and enable the most sig half 189
//      digitalWrite(s_write, HIGH);
//      digitalWrite(s_clk,HIGH);
//      delay(0.5);
//      digitalWrite(s_clk,LOW);
//      delay(0.5);
//      digitalWrite(s_write,LOW);
//      digitalWrite(s_clk,HIGH);
//      delay(0.5);
//      digitalWrite(s_clk,LOW);
//      delay(0.5);
//      digitalWrite(s_clk,HIGH);
//      delay(0.5);
//      digitalWrite(s_clk,LOW);
//      delay(0.5);
//      digitalWrite(s_clk,HIGH);
//      delay(0.5);
//      digitalWrite(s_clk,LOW);
//      delay(0.5);
//      //the command register now contains 1000 (lsb)
//  
//      //clock a value from the RAM
//      digitalWrite(s_cs,LOW);
//      digitalWrite(s_clk,HIGH);
//      delay(0.5);
//      digitalWrite(s_cs,HIGH);
//      digitalWrite(s_clk,LOW);
//      delay(0.5);
//
//      //read the value received
//      for(int i = 0;i<4;i++){
//        sample |= digitalRead(s_read) << i;
//        digitalWrite(s_clk, HIGH);
//        delay(0.5);
//        digitalWrite(s_clk, LOW);
//        delay(0.5);
//      }
//      int n_cycles_spent_waiting = 0;
//      //wait for the analyzer's clock to flip in order to read next value fro RAM
//      bool waiting_for_next_sample = true;
//      while (waiting_for_next_sample == true){
//        n_cycles_spent_waiting = n_cycles_spent_waiting + 1;
//        waiting_for_next_sample = !digitalRead(triggered);
//      }
//      int p_cycles_spent_waiting = 0;
//      waiting_for_next_sample = true;
//      while (waiting_for_next_sample == true){
//        p_cycles_spent_waiting = p_cycles_spent_waiting + 1;
//        waiting_for_next_sample = digitalRead(triggered);
//      }
//      //the analyzer is now addressing the next sample and the next iteration of the loop may occur. write the sample into the buffer at index.
//      sample_buffer[buffer_index] = sample;
//      
//      //Serial.println(sample);
//      //Serial.println(n_cycles_spent_waiting);
//      //Serial.println(p_cycles_spent_waiting);
//    }
//    String string_sample_buffer = "";
//    for(int i = 0;i<16;i++){
//      string_sample_buffer = string_sample_buffer + int(sample_buffer[i]) + " ";
//    }
//    Serial.println(string_sample_buffer);
//
//    //print the buffer to the serial console^^^
//    
//  
//
//}
