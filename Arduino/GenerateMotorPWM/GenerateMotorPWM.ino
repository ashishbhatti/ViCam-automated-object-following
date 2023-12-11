// Define a struct for storing the up and downtimes of the signal pulse
struct signalTimes {
  // All these times should be in microseconds
  unsigned long totalTime;
  unsigned long upTime;
  unsigned long downTime;
};
// to store the times
struct signalTimes yawMotorTime; 

struct motorSignalParams {
  // The min and max range of onTime accepted by the motor
  int minOnTime;
  int maxOnTime;
};

// setting yaw motor parameters
struct motorSignalParams yawMotor; 


float yawRate = 0;
float pitchRate = 0;

const int yawPin = 7;
const int pitchPin = 8;


// This function runs once
void setup() {

  pinMode(yawPin, OUTPUT);
  pinMode(pitchPin, OUTPUT);
  yawMotor.minOnTime = 1000;
  yawMotor.maxOnTime = 2000;

  // 50 Hz frequency, with 7.5% duty cycle results in 
  // 1500 microsecond
  // This results in stop motion for the motor
  // calcSignalTimes(50.0, 8.5, yawMotorTimes);
}


// Caculate the signal times
void calcSignalTimes(float frequency, float dutyCycle, struct signalTimes& signalTime) {
  /*
   Calculates the totalTime, upTime, and downTime of a pwm pulse.
   Args:
       float frequency: frequncy in Hz of your signal
       float dutyCycle: dutyCycle in percentage
       struct signalTime: struct to store the times 
  */
  signalTime.totalTime = 1000000.0 / frequency;
  signalTime.upTime =  dutyCycle * signalTime.totalTime / 100;
  signalTime.downTime = (100.0 - dutyCycle) * signalTime.totalTime /100; 
}



void generatePWMPulse(int pinNo, float rotationRate, struct signalTimes& signalTime) {
  /*
   Generates a software pwm pulse by setting pins high and low.
   Args:
       int pinNo: pin number which needs to controlled
       float rotationRate: the rotation rate of the motor, between -100.0 to 100.0
       struct signalTime: struct which stores the time information
  */
  int onTime = map(rotationRate, -100.0, 100.0, 1000, 2000);
  digitalWrite(pinNo, HIGH);
  delayMicroseconds(onTime);
  digitalWrite(pinNo, LOW);
  delayMicroseconds(2000 - onTime);
  delay(18);
}




// the loop function runs over and over again forever
void loop() {


  /* 
  // This code works DO NOT TOUCH
  // int onTime = map(10, -100.0, 100.0, 1100, 1900);
  digitalWrite(7, HIGH);
  delayMicroseconds(onTime);
  digitalWrite(7, LOW);
  delay(2000);
  */

  // struct signalTimes yawMotorTime;



  // // // Need to take input from serial for below
  yawRate = 0; // Declare pitchRate
  pitchRate = 0;

  // // // Generate PWM pulse using the calculated signal times
  generatePWMPulse(yawPin, yawRate, yawMotorTime);
  generatePWMPulse(pitchPin, pitchRate, yawMotorTime);

}













// void loop() {
//   /*
//   // This code works DO NOT TOUCH
//   digitalWrite(7, HIGH);   // turn the LED on (HIGH is the voltage level)
//   delayMicroseconds(1400);                       // wait for a second
//   digitalWrite(7, LOW);    // turn the LED off by making the voltage LOW
//   delay(2000);
//   */ }
