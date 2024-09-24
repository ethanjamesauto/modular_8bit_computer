int triggered  = 3;
int s_read  = 4;
int s_write     = 5;
int s_clk  = 6;
int s_cs  = 7;
int da_clear = 8;






void spi_write(byte to_send){
  for(int i = 0; i < 4; i++){
    digitalWrite(s_write,bitRead(to_send,i));
    digitalWrite(s_clk,true);
    delay(1);
    digitalWrite(s_clk,false);
    delay(1);
  }
  digitalWrite(s_write,LOW);
}

byte spi_read(){
  byte to_read;
  for(int i = 0;i < 4;i++){
    to_read |= digitalRead(s_read) << i;
    digitalWrite(s_clk,true);
    delay(1);
    digitalWrite(s_clk,false);
    delay(1);
  }
  for(int i = 4;i < 8;i++){
    to_read |= 0 << i;
  }
  return to_read;
}

String byte_to_string(byte toString){
  String returnString;
  for(int i = 0;i < 4;i++){
    char c[1];
    returnString = returnString + itoa(bitRead(toString,i),c,10);
  }
  return returnString;
}

void setup() {
    pinMode(triggered, INPUT);
    pinMode(s_read, INPUT);
    pinMode(s_write, OUTPUT);
    pinMode(s_clk, OUTPUT);
    pinMode(s_cs, OUTPUT);
    pinMode(da_clear, OUTPUT);
    Serial.begin(9600);
    //Serial.println("Begin Test");

    //disable the execution of commands:
    digitalWrite(s_cs, HIGH);
    digitalWrite(s_write, LOW);
    digitalWrite(s_clk,LOW);
    digitalWrite(da_clear,LOW);
    digitalWrite(da_clear,HIGH);

    spi_write(0b00001110);
    //spi_write(test_byte);
    for(int i = 0;i<4;i++){
      //Serial.println(!digitalRead(s_read));
      digitalWrite(s_clk,HIGH);
      delay(1);
      digitalWrite(s_clk,LOW);
      delay(1);
    }
    


}

void loop() {
    //send clear command
    digitalWrite(da_clear,LOW);
    delay(1);
    digitalWrite(da_clear,HIGH);
    delay(1);

    //clear command register
    spi_write(0b00000000);


    //wait for trigger
    bool not_triggered = true;
    while (not_triggered == true){
      not_triggered = digitalRead(triggered);
      delay(1);
      //Serial.println("waiting for trigger");
    }

    byte sample_buffer[16];

    //once trigger has been seen, read first value from buffer then halt.
    //at this point, the command register is still 0000 (lsb) and the least sig half buffer 189 is selected.
    //Serial.println("TRIGGERED. READING BUFFER:");
    for(int buffer_index = 0; buffer_index < 16; buffer_index++){
      byte sample = 0b00000000;
   
    
      //clock a value from the RAM
      digitalWrite(s_cs,LOW);
      digitalWrite(s_clk,HIGH);
      delay(0.5);
      digitalWrite(s_cs,HIGH);
      digitalWrite(s_clk,LOW);
      delay(0.5);

      //read the value received
      for(int i = 4;i<8;i++){
        sample |= digitalRead(s_read) << i;
        digitalWrite(s_clk, HIGH);
        delay(0.5);
        digitalWrite(s_clk, LOW);
        delay(0.5);
      }

      //disable the least sig half 189 and enable the most sig half 189
      digitalWrite(s_write, HIGH);
      digitalWrite(s_clk,HIGH);
      delay(0.5);
      digitalWrite(s_clk,LOW);
      delay(0.5);
      digitalWrite(s_write,LOW);
      digitalWrite(s_clk,HIGH);
      delay(0.5);
      digitalWrite(s_clk,LOW);
      delay(0.5);
      digitalWrite(s_clk,HIGH);
      delay(0.5);
      digitalWrite(s_clk,LOW);
      delay(0.5);
      digitalWrite(s_clk,HIGH);
      delay(0.5);
      digitalWrite(s_clk,LOW);
      delay(0.5);
      //the command register now contains 1000 (lsb)
  
      //clock a value from the RAM
      digitalWrite(s_cs,LOW);
      digitalWrite(s_clk,HIGH);
      delay(0.5);
      digitalWrite(s_cs,HIGH);
      digitalWrite(s_clk,LOW);
      delay(0.5);

      //read the value received
      for(int i = 0;i<4;i++){
        sample |= digitalRead(s_read) << i;
        digitalWrite(s_clk, HIGH);
        delay(0.5);
        digitalWrite(s_clk, LOW);
        delay(0.5);
      }
      int n_cycles_spent_waiting = 0;
      //wait for the analyzer's clock to flip in order to read next value fro RAM
      bool waiting_for_next_sample = true;
      while (waiting_for_next_sample == true){
        n_cycles_spent_waiting = n_cycles_spent_waiting + 1;
        waiting_for_next_sample = !digitalRead(triggered);
      }
      int p_cycles_spent_waiting = 0;
      waiting_for_next_sample = true;
      while (waiting_for_next_sample == true){
        p_cycles_spent_waiting = p_cycles_spent_waiting + 1;
        waiting_for_next_sample = digitalRead(triggered);
      }
      //the analyzer is now addressing the next sample and the next iteration of the loop may occur. write the sample into the buffer at index.
      sample_buffer[buffer_index] = sample;
      
      //Serial.println(sample);
      //Serial.println(n_cycles_spent_waiting);
      //Serial.println(p_cycles_spent_waiting);
    }
    String string_sample_buffer = "";
    for(int i = 0;i<16;i++){
      string_sample_buffer = string_sample_buffer + int(sample_buffer[i]) + " ";
    }
    Serial.println(string_sample_buffer);

    //print the buffer to the serial console^^^
    
  

}
