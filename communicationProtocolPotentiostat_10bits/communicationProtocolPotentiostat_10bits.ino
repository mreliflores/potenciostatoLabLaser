#include <TimerOne.h>

String str;
String strs[9];
int q;

int pwm=9;

int tech;
String sync_fromApp = "?";
String sync_ok = "okx";

int cyc_num;
int PWM_0;
int PWM_i;
int PWM_f;

float volt;
float cur;
int t;

void setup() {
  // put your setup code here, to run once:
  Timer1.initialize(140);
  Serial.begin(9600);
  Serial.setTimeout(5);
  pinMode(A0, INPUT);
  pinMode(pwm, OUTPUT);
  Timer1.pwm(pwm, 510);
  delay(1000);
}

void loop() {
  // put your main code here, to run repeatedly:
  int strCount = 0;
  if (Serial.available() > 0) {
    
    str = Serial.readString();
    str.trim();
    
    if (str == sync_fromApp) {
      Serial.println(sync_ok);
      //Serial.flush();
    }

    while (str.length() > 0) {
      int index = str.indexOf('x');
      if (index == -1) {
        strs[strCount++] = str;
        break;
      }
      else {
        strs[strCount++] = str.substring(0, index);
        str = str.substring(index + 1);
      }
    }

    tech = strs[0].toInt();
    float E0 = strs[1].toInt() / 1000.0;
    float Ei = strs[2].toInt() / 1000.0;
    float Ef = strs[3].toInt() / 1000.0;
    cyc_num = strs[4].toInt();
    int scan_rate = strs[5].toInt();
    int t_chro = strs[6].toInt();
    int t_step_chro = strs[7].toInt();
    int t_stab = strs[8].toInt();
    
    float e00 = ((9970.0 / (9970+9960)) * 5.03 + (9970.0 / 9860.0) * E0);
    PWM_0 = e00 * (1023 / 4.97); //Starting Voltage
    float eii = ((9970.0 / (9970+9960)) * 5.03 + (9970.0 / 9860.0) * Ei);
    PWM_i = eii * (1023 / 4.97); //Min Voltage
    float eff = ((9970.0 / (9970+9960)) * 5.03 + (9970.0 / 9860.0) * Ef);
    PWM_f = eff * (1023 / 4.97); //Max Voltage
    long t = (4960000L) / (1024L * scan_rate); //delay scan rate
    int t_count = t_chro/t_step_chro;

    if (PWM_f > 1023 || PWM_i > 1023 || PWM_0 > 1023){
      if (PWM_f > 1023){
        PWM_f = 1023;
      }
      else if (PWM_i > 1023){
        PWM_i = 1023;
      }
      else if (PWM_0 > 1023){
        PWM_0 = 1023;
      }
    }

    if (PWM_f < 0 || PWM_i < 0 || PWM_0 <0){
      if (PWM_f < 0){
        PWM_f = 0;
      }
      else if (PWM_i < 0){
        PWM_i = 0;
      }
      else if (PWM_0 < 0){
        PWM_0 = 0;
      }
    }
    
    switch (tech) {
      //---Cyclic voltammetry---
      case 1:
        Timer1.pwm(pwm, PWM_0);
        delay(t_stab);
        for (int n = 1; n <= cyc_num  && !Serial.available(); n++) {
          for (int val = PWM_0; val < PWM_f  && !Serial.available(); val++) {
            Timer1.pwm(pwm, val);

            volt = 0.0048046584*val-2.490;
            cur = 0.4935*analogRead(A0)-249.145;

            Serial.print(volt, 3);
            Serial.print('x');
            Serial.print(cur, 3);
            Serial.println('x');
            Serial.flush();
            //if (Serial.available() > 0){
              //delay(1000);
              //Serial.println("Nx");
              //break;
            //}
            delay(t);
            //if (Serial.available() > 0){
              //delay(1000);
              //Serial.println("Nx");
              //break;
            //}
            
          }

          for (int val = PWM_f; val > PWM_i  && !Serial.available(); val--) {
            Timer1.pwm(pwm, val);
            
            volt = 0.0048046584*val-2.490;
            cur = 0.4935*analogRead(A0)-249.145;
            //cur_ave = analogRead(A0);
            Serial.print(volt, 3);
            Serial.print('x');
            Serial.print(cur, 3);
            Serial.println('x');
            Serial.flush();
            //if (Serial.available() > 0){
              //delay(1000);
              //Serial.println("Nx");
              //break;
            //}
            delay(t);
            //if (Serial.available() > 0){
              //delay(1000);
              //Serial.println("Nx");
              //break;
            //}
          }
          PWM_0 = PWM_i;
        }
        Serial.println("Nx");
        Serial.flush();
        Timer1.pwm(pwm, 510);
        tech = 0;
        break;
      // ---------------Linear voltammetry-----------
      case 3:
        for (int n = 1; n <= cyc_num && !Serial.available(); n++) {
          Timer1.pwm(pwm, PWM_i);
          delay(t_stab);
          for (int val = PWM_i; val < PWM_f  && !Serial.available(); val++) {
            Timer1.pwm(pwm, val);

            volt = 0.0048046584*val-2.490;
            cur = 0.4935*analogRead(A0)-249.145;

            Serial.print(volt, 3);
            Serial.print('x');
            Serial.print(cur, 3);
            Serial.println('x');
            Serial.flush();
            /*if (Serial.available() > 0){
              delay(1000);
              Serial.println("Nx");
              break;
            }*/
            delay(t);
            /*if (Serial.available() > 0){
              delay(1000);
              Serial.println("Nx");
              break;
            }*/
          } 
        }
        Serial.println("Nx");
        Serial.flush();
        Timer1.pwm(pwm, 510);
        tech = 0;
        break;
      // ------------Chronoamperometry--------------
      case 2:
        for (int n = 1; n<=t_count && !Serial.available(); n++){
          Timer1.pwm(pwm, PWM_0);
          cur = 0.4935 * (analogRead(A0)) - 249.145;
          Serial.print(cur, 3);
          Serial.println('x');
          Serial.flush();
         /* if (Serial.available() > 0){
            delay(1000);
            Serial.println("Nx");
            break;
          }*/
          delay(t_step_chro*1000);
          /*if (Serial.available() > 0){
            delay(1000);
            Serial.println("Nx");
            break;
          }*/
        }
        Serial.println("Nx");
        Serial.flush();
        Timer1.pwm(pwm, 510);
        tech = 0;
        break;
    }
  }
  
  else {
    digitalWrite(13, HIGH);
    delay(200);
    digitalWrite(13, LOW);
    delay(200);
  }
}
