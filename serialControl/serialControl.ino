#include <LiquidCrystal.h>
const int rs = 51, en = 47, d4 = 37, d5 = 35, d6 = 33, d7 = 31;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
int j = 0;
int i = 0;
void setup() {
    Serial.begin(9600);
    lcd.begin(16, 2);
}

void loop() {
  
  lcd.setCursor(7, 1);
  lcd.print(j);
  j++;
  char cbuff[40];
  while(Serial.available()>0){
    char x = Serial.read();
    if(x!=10){
      lcd.setCursor(i,0);
      i++;
      lcd.write(x);
      Serial.println(x);
    }
    else{
      lcd.setCursor(0, 0);
      lcd.print("                ");
      i=0;
    }
  
    }
    i=0;
    
  
  

  //i++;
  //i=0;
  delay(500);
}

