#include <Wire.h>
#include "controllerinfo.h"

Player player;

int address, prev_address;
byte field, incoming_size;

bool transfer_state, done;

void setup() {
  transfer_state = 0;
  address = DEFAULT_ADDRESS;
  done = 0;
  
  Wire.begin(address);          
  Wire.onRequest(acknowledge);      
  Wire.onReceive(assignAddress);
  Serial.begin(9600);
  
  while(address == DEFAULT_ADDRESS) {delay(100);}
  Wire.end();
  Wire.begin(address);
  Wire.onRequest(requestHandler); 
  Wire.onReceive(receptionHandler);
}

void loop() {
  if(digitalRead(EXIT_BUTTON_PIN)) {
    Wire.end();
    prev_address = address;
    address = EXIT_ADDRESS;
    Wire.begin(address);
    Wire.onRequest(requestHandler);
    Wire.onReceive(receptionHandler);
    while(!done) {delay(100);}
    Wire.end();
    while(1);
  }
  
  delay(100);
}

void assignAddress(int num_bytes) {
  address = Wire.read();
}

void requestHandler() {
  if(transfer_state) {
    switch(field) {
      case HEALTH_FIELD:
        Wire.write(player.health);
        break;
      case SKILLPOINTS_FIELD:
        Wire.write(player.skillpoints);
        break;
      case ITEMS_OBTAIN_FIELD:
        // Should not get here!
        break;
      case ITEMS_LOSE_FIELD:
        // Should not get here!
        break;
      case ITEMS_LOOK_FIELD:
        Wire.write(player.items);
        break;
      case PLAYERNAME_FIELD:
        Wire.write(player.playername, PLAYERNAME_MAX_SIZE);
        break;
      case PREVIOUS_ADDRESS_FIELD:
        Wire.write(prev_address);
        break;
      case DONE_FIELD:
        // Should not get here!
        break;
    }
  } else {
    // Should not get here!
  }
}

void receptionHandler(int num_bytes) {
  if(transfer_state) {
    switch(field) {
      case HEALTH_FIELD:
        player.health = READ_INT();
        break;
      case SKILLPOINTS_FIELD:
        player.skillpoints = READ_INT();
        break;
      case ITEMS_OBTAIN_FIELD:
        player.items /= READ_INT();
        break;
      case ITEMS_LOSE_FIELD:
        player.items &= ~(READ_INT());
        break;
      case ITEMS_LOOK_FIELD:
        player.items = READ_INT();
      case PLAYERNAME_FIELD:
        for(int i = 0; i < incoming_size; i++) player.playername[i] = Wire.read();
        for(int i = incoming_size; i < 16; i++) player.playername[i] = 0;
        break;
      case PREVIOUS_ADDRESS_FIELD:
        // Should not get here!
        break;
      case DONE_FIELD:
        if(address == EXIT_ADDRESS) done = 1;
        break;
    }
  } else {
    field = Wire.read();
    incoming_size = Wire.read();
  }
}

void acknowledge() {
  Wire.write(1);
}
