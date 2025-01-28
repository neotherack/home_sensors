#include "config.h"

#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

#include <DHT.h>
#include <Wire.h>
#include <BMP180I2C.h>

// static
// use https://www.calcmaps.com/map-elevation/
#define PA_TO_mBAR 100
#define I2C_ADDRESS 0x77
#define DHT22_PIN 0

const int LED = 1;
const int ADC = A0;

// Custom types
typedef struct
{
  float temperature;
  float pressure;
}
bmp180_data_type;

typedef struct
{
  float temperature;
  float humidity;
}
dht22_data_type;

typedef struct
{
  float ppm;
}
mics5524_data_type;


// vars
ESP8266WebServer server(PORT);
BMP180I2C bmp180(I2C_ADDRESS);
DHT dht22(DHT22_PIN, DHT22);

// measurements
dht22_data_type dht22_data;
bmp180_data_type bmp180_data;
mics5524_data_type mics5524_data;

// wifi
void connect_wifi()
{
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("connected");
  Serial.print("Use this URL: ");
  Serial.print("http://");
  Serial.print(WiFi.localIP());
  Serial.println("/");
}

// Sensor methods
void read_dht22()
{
  dht22_data.humidity  = dht22.readHumidity();
  dht22_data.temperature = dht22.readTemperature();
}

void read_bmp180()
{
  if (!bmp180.measureTemperature())
  {
	  Serial.println("could not start temperature measurement, is a measurement already running?");
	  return;
  }

  do
  {
	  delay(100);
  } while (!bmp180.hasValue());

  if (!bmp180.measurePressure())
  {
	  Serial.println("could not start perssure measurement, is a measurement already running?");
	  return;
  }

  do
  {
	delay(100);
  } while (!bmp180.hasValue());

  bmp180_data.temperature = bmp180.getTemperature() + TEMPERATURE_FIX;
  bmp180_data.pressure = (bmp180.getPressure() / PA_TO_mBAR) + PRESSURE_FIX;
}

void read_mics5524()
{
  mics5524_data.ppm = analogRead(ADC);
}


void read_sensors()
{
  read_dht22();
  read_bmp180();
  read_mics5524();
}

// webserver
String build_metric(String metric_name, String metric_type, String metric_description, float metric_value)
{
  String res = "# HELP "+metric_name+" "+metric_description+"\n"+
         "# TYPE "+metric_name+" "+metric_type+"\n"+
         metric_name+" "+metric_value+"\n";
  return res;
}

String get_metrics()
{
  String response="";
  int64_t time;
  time = millis();

  read_sensors();
  
  response += build_metric("time_seconds_total","counter","seconds from boot", time);
  response += build_metric("free_memory","gauge","free memory", 1.0);
  response += build_metric("bmp180_temperature","gauge","temperature on bmp180", bmp180_data.temperature);
  response += build_metric("bmp180_pressure","gauge","pressure on bmp180", bmp180_data.pressure);
  response += build_metric("dht22_temperature","gauge","temperature on dht22", dht22_data.temperature);
  response += build_metric("dht22_humidity","gauge","humidity on dht22", dht22_data.humidity);
  response += build_metric("mics5524_ppm","gauge","gas on mics5524, ppm", (float) mics5524_data.ppm);

  return response;
}

void handleMetrics() {
  server.send(200, "text/plain", get_metrics());
}

void handleNotFound(){
  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET)?"GET":"POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";
  for (uint8_t i=0; i<server.args(); i++){
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
  }
  server.send(404, "text/plain", message);
}

void led_blink()
{
  digitalWrite(LED, 1);
  delay(1000);
  digitalWrite(LED, 0);
}



void scan_i2c() 
{
  String response="";
  byte error, address;
  int nDevices;

  nDevices = 0;
  for(address = 1; address < 127; address++ ) {
    Wire.beginTransmission(address);
    error = Wire.endTransmission(true);
    String add_str = (String) address;
    String err_str = (String) error;
    if (error == 0) 
    {
      response+=">>>>> I2C device found at address "+add_str+"!\n";
      nDevices++;
    }
    else
    {
      response+="I2C device error "+err_str+" at address "+add_str+"\n";
    }
  }
  if (nDevices == 0) {
    response+="No I2C devices found\n";
  }
  server.send(200, "text/plain", response);
}

void setup() {
  Serial.begin(9600);
  connect_wifi();

  Wire.begin();
  dht22.begin(); // initialize the DHT22 sensor
  bmp180.begin(); // initialize the BMP180 sensor
  //bmp180.resetToDefaults();
  //bmp180.setSamplingMode(BMP180MI::MODE_UHR);

  server.on("/", handleMetrics);
  server.on("/metrics", handleMetrics);
  server.on("/debug", scan_i2c);
  server.onNotFound(handleNotFound);
  server.begin();

  Serial.println("HTTP server started");
}


void loop() 
{
  server.handleClient();
}
