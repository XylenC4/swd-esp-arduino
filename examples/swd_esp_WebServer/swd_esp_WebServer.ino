#include <WiFi.h>
#include <WebServer.h>
#include <swd_host.h>
#include <credentials.h>
#include <ArduinoOTA.h>

// Shared objects
WebServer server(80);

#define CONFIG_ESP_SWD_CLK_PIN 16
#define CONFIG_ESP_SWD_IO_PIN 15
#define CONFIG_ESP_SWD_NRST_PIN 17
#define SRAM_START 0x20000000
#define SRAM_SIZE  (20 * 1024)  // 20KB

// Function declarations
void setup_WIFI();
void loop_WIFI();
void setup_WebServer();
void loop_WebServer();
void setup_SWD();
void loop_SWD();

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("Booting...");

  setup_SWD();
  setup_WIFI();
  setup_WebServer();
  setup_OTA();
}

void loop() {
  loop_WIFI();
  loop_WebServer();
  loop_SWD();  // Currently unused, but available for future use
  loop_OTA();
}