#include "ESP8266WiFi.h"
#include "DHT.h"
#define DHTPIN 2    // what digital pin we're connected to
#define soilpin 3
#define ldrpin A0        //pin2 to D4 on esp board, pin3 to D5 

#define DHTTYPE DHT11  // DHT 11


DHT dht(DHTPIN,DHTTYPE);
float soilvalue,ldrvalue,humidityvalue,temperaturevalue;

const char WEBSITE[] = "api.pushingbox.com"; //pushingbox API server
const String devid = "vE05AFC3877EFF57"; //device ID from Pushingbox 

const char* MY_SSID = "";
const char* MY_PWD =  "";


void setup()
{
  Serial.begin(115200);
  dht.begin();
  Serial.print("Connecting to "+*MY_SSID);
  WiFi.begin(MY_SSID, MY_PWD);
  Serial.println("going into wl connect");

  while (WiFi.status() != WL_CONNECTED) //not connected,..waiting to connect
    {
      delay(1000);
      Serial.print(".");
    }
  Serial.println("wl connected");
  Serial.println("");
  Serial.println("Credentials accepted! Connected to wifi\n ");
  Serial.println("");
}


void loop()
{
  delay(10000); //10 seconds, (sampling rate vs. service call quota)

  humidityvalue = dht.readHumidity();
  // Read temperature as Celsius (the default)
  temperaturevalue = dht.readTemperature();
  ldrvalue=analogRead(ldrpin);
  soilvalue = analogRead(soilpin);

  // Check if any reads failed and exit early (to try again).
  if (isnan(humidityvalue) || isnan(temperaturevalue) || isnan(ldrvalue)|| isnan(soilvalue))
  {
    Serial.println("Failed to read from the sensors!");
    return;
  }


  //Print to Serial monitor or Terminal of your chocice at 115200 Baud
  Serial.print("Temperature: ");
  Serial.print(temperaturevalue);
  Serial.print(" *C\t");
  Serial.print("humidity: ");
  Serial.print(humidityvalue);
  Serial.print(" % ");
  Serial.print("Soil moisture: ");
  Serial.print(soilvalue);
  Serial.print(" mm/growth period\t");
  Serial.print("Light intensity: ");
  Serial.print(ldrvalue);
  Serial.print(" K ohm ");
  
    
  WiFiClient client;  //Instantiate WiFi object

    //Start or API service using our WiFi Client through PushingBox
    if (client.connect(WEBSITE, 80))
      { 
         client.print("GET /pushingbox?devid=" + devid
       + "&temperature=" + (String) temperaturevalue
       + "&humidity="      + (String) humidityvalue
       + "&soilmoisture="     + (String) soilvalue
       + "&lightintensity="      + (String) ldrvalue
       
         );

      client.println(" HTTP/1.1"); 
      client.print("Host: ");
      client.println(WEBSITE);
      client.println("User-Agent: ESP8266/1.0");
      client.println("Connection: close");
      client.println();
      }
}
