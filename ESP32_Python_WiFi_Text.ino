#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "OnePlus 11 5G";
const char* password = "9717724888#";

WebServer server(80);

String outbox = "";

void handleReceive() {
  if (server.hasArg("plain")) {
    String msg = server.arg("plain");
    Serial.println("[Python] " + msg);
    outbox = "";
  }
  server.send(200, "text/plain", "OK");
}

void handleSend() {
  server.send(200, "text/plain", outbox);
  outbox = "";
}

void setup() {
  Serial.begin(115200);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.printf("\nIP: %s\n", WiFi.localIP().toString().c_str());

  server.on("/send", HTTP_POST, handleReceive);
  server.on("/recv", HTTP_GET, handleSend);
  server.begin();
  Serial.println("Chat server ready.");
}

void loop() {
  server.handleClient();

  if(Serial.available()) {
    String line = Serial.readStringUntil('\n');
    line.trim();
    if (line.length()) {
      outbox = line;
      Serial.println("[ESP32] " + line);
    }
  }

  delay(1);
}