#include <swd_host.h>

#define CONFIG_ESP_SWD_CLK_PIN 16
#define CONFIG_ESP_SWD_IO_PIN 15
#define CONFIG_ESP_SWD_NRST_PIN 17

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("Starting SWD...");

  // Set SWD pins
  //swd_set_pins(SWDIO_PIN, SWCLK_PIN);

  // Initialize SWD interface
  swd_init_debug();

  uint32_t idcode = 0;
  if (swd_read_idcode(&idcode)) {
    Serial.print("IDCODE: 0x");
    Serial.println(idcode, HEX);
  } else {
    Serial.println("Failed to read IDCODE.");
  }

  // Optionally halt the core before reading memory
  //swd_halt_target();
  //swd_wait_until_halted();
}

void loop() {
  // Nothing to do here
}