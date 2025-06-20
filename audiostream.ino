#include <WiFi.h>
#include <WiFiUdp.h>
#include "driver/i2s.h"

// I2S configuration
#define I2S_SAMPLE_RATE   44100
#define I2S_BITS_PER_SAMPLE 16

i2s_config_t i2s_config = {
  .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_TX),
  .sample_rate = I2S_SAMPLE_RATE,
  .bits_per_sample = (i2s_bits_per_sample_t)I2S_BITS_PER_SAMPLE,
  .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT, // Mono output (left channel)
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
// WiFi credentials
const char* ssid     = "TP-Link";
const char* password = "apalah123";

WiFiUDP udp;
const unsigned int localUdpPort = 5005;
char incomingPacket[8192]; // Buffer untuk data UDP

void startI2S() {
  i2s_driver_install(I2S_NUM_0, &i2s_config, 0, NULL);
  i2s_set_pin(I2S_NUM_0, &pin_config);
}

void setup() {
  Serial.begin(115200);
  startI2S();
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.print("\nIP address: ");
  Serial.println(WiFi.localIP());
  Serial.println("\nWiFi connected");
  udp.begin(localUdpPort);
  Serial.printf("Listening UDP on port %d\n", localUdpPort);
}

void loop() {
  int packetSize = udp.parsePacket();
  if (packetSize) {
    int len = udp.read(incomingPacket, sizeof(incomingPacket));
    if (len > 0) {
      int16_t* samples = (int16_t*)incomingPacket;
      size_t num_samples = len / sizeof(int16_t);
      size_t bytes_written = 0;
      i2s_write(I2S_NUM_0, samples, num_samples * sizeof(int16_t), &bytes_written, portMAX_DELAY);
    }
  }
}