#include <SparkFunESP8266WiFi.h>
#include <PubSubClient.h>
//#include <SoftwareSerial.h>
const char mySSID[] = "Asus-NET";
const char myPSK[] = "RJ110209";
const char* server = "IP Address";

ESP8266Client espClient;
PubSubClient client(espClient);
char message_buff[3];

void setup(){
  //Serial.begin(9600);
  esp8266.begin();
 // Serial.println("Started");
  esp8266.setMode(ESP8266_MODE_STA);
  if (esp8266.status() <= 0){
    while(esp8266.connect(mySSID, myPSK) < 0){
   //   Serial.println("Error connecting");
      delay(60000);
    }    
  }
 // Serial.print("My IP address is: ");
 // Serial.println(esp8266.localIP());
  //Serial.print("Connecting...");
  client.setServer(server, 1883);
  if(client.connect("arduinoClient")){
    while(true){
      String pubString = "" + String(analogRead(A0)) + "";
      pubString.toCharArray(message_buff, pubString.length()+1);
      client.publish("/sensor/moisture", message_buff);
      //Serial.println("Publishing");
      delay(120000);
    }
  }
//  else{
 //   Serial.println("failed");
//    Serial.print("RC: ");
//    Serial.println(client.state());
//  }
}

void loop(){
//  client.loop();
}




