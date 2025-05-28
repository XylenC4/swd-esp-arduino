extern WebServer server;
uint8_t* readSRAM(size_t& outSize);  // From SWD.ino

void setup_WebServer() {
  server.on("/SRAM.bin", HTTP_GET, []() {
    size_t size;
    uint8_t* buffer = readSRAM(size);

    if (!buffer) {
      server.send(500, "text/plain", "Failed to read memory.");
      return;
    }

    server.sendHeader("Content-Type", "application/octet-stream");
    server.sendHeader("Content-Disposition", "attachment; filename=\"SRAM.bin\"");
    server.sendHeader("Connection", "close");
    server.send_P(200, "application/octet-stream", (const char*)buffer, size);

    free(buffer);
  });

  server.begin();
  Serial.println("HTTP server started");
}

void loop_WebServer() {
  server.handleClient();
}