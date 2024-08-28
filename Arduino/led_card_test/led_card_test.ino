int data_pins[] = {2,3,4,5,6,7,8,9};
int addr_pins[] = {A0,A1,A2,A3};
int we_pin = 10;

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);

  for (int i = 0; i < 8; i++) pinMode(data_pins[i], OUTPUT);
  for (int i = 0; i < 4; i++) pinMode(addr_pins[i], OUTPUT);
  pinMode(we_pin, OUTPUT);
  digitalWrite(we_pin, HIGH);
}

void do_write(uint8_t data, uint8_t addr) {
  for (int i = 0; i < 8; i++) digitalWrite(data_pins[i], (data >> i) & 1);
  for (int i = 0; i < 4; i++) digitalWrite(addr_pins[i], (addr >> i) & 1);
  delay(4);
  digitalWrite(we_pin, LOW);
  delay(5);
  digitalWrite(we_pin, HIGH);
  delay(1);
}

// the loop function runs over and over again forever
void loop() {
  // digitalWrite(LED_BUILTIN, HIGH);  // turn the LED on (HIGH is the voltage level)
  // delay(1000);                      // wait for a second
  // digitalWrite(LED_BUILTIN, LOW);   // turn the LED off by making the voltage LOW
  // delay(1000);                      // wait for a second
  for (int i = 0; i < 16; i++) {
    uint8_t dat = 0b10101010;
    if (i % 2 == 1) dat ^= 0xff;
    do_write(dat, i);
  }
  delay(5000);
}
