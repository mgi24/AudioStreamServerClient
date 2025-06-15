#include <WiFi.h>
#include "driver/i2s.h"

// WiFi credentials
const char* ssid     = "TP-Link";
const char* password = "apalah123";

// Server TCP
const char* host = "192.168.0.100"; // Ganti dengan IP server Anda
const uint16_t port = 12345;

// Audio config
#define SAMPLE_RATE   44100
#define I2S_NUM       I2S_NUM_0
#define BUFFER_SIZE   1024

WiFiClient client;

void setup_wifi() {
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");
}

void setup_i2s() {
  i2s_config_t i2s_config = {
    .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_TX),
    .sample_rate = SAMPLE_RATE,
    .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
    .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT, // Mono (left channel only)
    .communication_format = I2S_COMM_FORMAT_I2S,
    .intr_alloc_flags = 0,
    .dma_buf_count = 8,
    .dma_buf_len = 512,
    .use_apll = false,
    .tx_desc_auto_clear = true,
    .fixed_mclk = 0
  };

  i2s_pin_config_t pin_config = {
      .mck_io_num = 3,                 // MCLK pin
      .bck_io_num = 19,                // BCK pin
      .ws_io_num = 21,                 // LRCK pin
      .data_out_num = 18,              // DATA out pin
      .data_in_num = I2S_PIN_NO_CHANGE // Not used
  };

  i2s_driver_install(I2S_NUM, &i2s_config, 0, NULL);
  i2s_set_pin(I2S_NUM, &pin_config);
}

void setup() {
  Serial.begin(115200);
  setup_wifi();
  setup_i2s();

  Serial.print("Connecting to server...");
  while (!client.connect(host, port)) {
    Serial.print(".");
    delay(1000);
  }
  Serial.println("\nConnected to server!");
}

void loop() {
  static uint8_t buffer[BUFFER_SIZE];
  if (client.connected()) {
    int bytesRead = client.read(buffer, BUFFER_SIZE);
    if (bytesRead > 0) {
      size_t bytes_written = 0;
      i2s_write(I2S_NUM, buffer, bytesRead, &bytes_written, portMAX_DELAY);
    }
  } else {
    Serial.println("Disconnected from server, reconnecting...");
    while (!client.connect(host, port)) {
      delay(1000);
    }
    Serial.println("Reconnected!");
  }
}