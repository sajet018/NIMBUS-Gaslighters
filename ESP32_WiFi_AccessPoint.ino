#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "Team Gaslighters";
const char* password = "gaslighters"
WebServer server(80);

String lastMessage = "No message yet.";

void handleHome() {
  Serial.println("Homepage requested");
  
  String html = "";

  html += "<!DOCTYPE html>";
  html += "<html>";
  html += "<head>";
  html += "<title>ESP32 Chat</title>";
  html += "<meta name='viewport' content='width=device-width, initial-scale=1'>";
  html += "</head>";
  html += "<body style='font-family: Arial, padding: 20px;'>";

  html += "<h2>Phone to ESP32</h2>";

  html += "<form action='/send' method='GET'>";
  html += "<input name='msg' placeholder='Type message' style='font-size:20px; width:90%'>";
  html += "<br><br>";
  html += "<button type='submit' style='font-size:20px;'>Send</button>";
  html += "</form>";

  html += "<h3>Last message received by ESP32:</h3>";
  html += "<p style='font-size:24px; color:blue;'>" + lastMessage + "</p>";

  html += "</body>";
  html += "</html>";

  server.send(200, "text/html", html);
}

void handleSend() {
  Serial.println("Send route requested.");

  if (server.hasArg("msg")) {
    lastMessage = server.arg("msg");

    Serial.print("Message from phone: ");
    Serial.println(lastMessage);
  }
  else {
    Serial.println("No msg argument received.");
  }

  server.sendHeader("Location", "/");
  server.send(303);
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println();
  Serial.println("Starting ESP32...");

  WiFi.mode(WIFI_AP);

  bool success = WiFi.softAP(ssid, password);

  if (success) {
    Serial.println("ESP32 WiFi started successfully.");
  }
  else {
    Serial.println("Failed to start ESP32 WiFi.");
  }

  Serial.print("Connect phone to WiFi: ");
  Serial.println(ssid);

  Serial.print("Password: ");
  Serial.println(password);

  Serial.print("ESP32 IP address: ");
  Serial.println(WiFi.softAPIP());

  server.on("/", handleHome);
  server.on("/send", handleSend);
  
  server.begin();

  Serial.println("Server started.");
  Serial.println("Open this in your browser:");
  Serial.print("http://");
  Serial.println(WiFi.softAPIP());
}

void loop() {
  server.handleClient();
}