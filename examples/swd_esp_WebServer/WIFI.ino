extern WebServer server;
const char* ssid = mySSID;
const char* password = myPassword;

void setup_WIFI() {
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConnected to WiFi. IP address:");
  Serial.println(WiFi.localIP());
}

void loop_WIFI() {
  // Reserved for future logic (e.g., reconnect or OTA handling)
}