int lightPin = 0;  //define a pin for Photo resistor



void setup()

{

Serial.begin(19200);  //Begin serial communcation

}



void loop()

{
Serial.println(analogRead(lightPin));
delay(1); //short delay for faster response to light.
//delayMicroseconds(50)

}
