#define FSYNC   5
#define SCLK    4
#define SDATA   14

enum op_mode {SINE = 0B00, TRIANGLE = 0B01, SQUARE = 0B10};

void writeReg(uint16 word16){
  digitalWrite(SCLK, LOW);
  digitalWrite(SCLK, HIGH);
  digitalWrite(FSYNC, LOW);
  
  for(int8 i = 15; i >=0; i--){
    digitalWrite(SDATA, (word16 >> i) & 1);
    digitalWrite(SCLK, LOW);
    digitalWrite(SCLK, HIGH); 
  }
  
  digitalWrite(FSYNC, HIGH);
}

void setFrequency(uint32 freq, uint8 MODE){
  //if (freq >> 28) Serial.println("frequency bigger than 28 bits");
  freq = freq & 0x0FFFFFFF;
  writeReg(0x2008 | ( (MODE & 2) << 4 ) | ( (MODE & 1) << 1 ));
  writeReg(0x4000 | (freq & 0x3FFF));
  writeReg(0x4000 | ( (freq >> 14) & 0x3FFF) );
}

void setup() {
   pinMode(FSYNC, OUTPUT);
   pinMode(SCLK, OUTPUT);
   pinMode(SDATA, OUTPUT);
   
   Serial.begin(250000);
   Serial.setTimeout(500);

   digitalWrite(FSYNC, HIGH);
   digitalWrite(SCLK, HIGH);
   delay(500);
   
   writeReg(0x1000);
   writeReg(0x4002);
   
}

uint32 f = 0;
byte b;

void loop() {
   if (Serial.available()){
    b = Serial.read();
    if (b & 0x80){
      f = b & (0x7f);
      for(int i = 7; i <= 21; i+= 7)
        f |= Serial.read() << i;
      uint8 mod = Serial.read();
      if ( (f < 0x0C000000) && (mod < 3) )
        setFrequency(f, mod);
    }
   }
   
   //Serial.println("jinx");
}
