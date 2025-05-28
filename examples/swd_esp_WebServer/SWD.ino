#include <Arduino.h>

#define SRAM_START 0x20000000
#define SRAM_SIZE (20 * 1024)  // 20KB

void setup_SWD() {
  Serial.println("Starting SWD...");
  swd_init_debug();

  uint32_t idcode = 0;
  if (swd_read_idcode(&idcode)) {
    Serial.printf("IDCODE: 0x%08X\n", idcode);
    //swd_halt_target();
    //swd_wait_until_halted();
  } else {
    Serial.println("Failed to read IDCODE.");
  }
}

void loop_SWD() {
  // Optional: future SWD interaction
}

uint8_t* readSRAM(size_t& outSize) {
  uint8_t* buffer = (uint8_t*)malloc(SRAM_SIZE);
  if (!buffer) {
    Serial.println("Memory allocation failed.");
    outSize = 0;
    return nullptr;
  }

  if (!swd_read_memory(SRAM_START, buffer, SRAM_SIZE)) {
    Serial.println("Failed to read memory.");
    free(buffer);
    outSize = 0;
    return nullptr;
  }

  outSize = SRAM_SIZE;
  return buffer;
}