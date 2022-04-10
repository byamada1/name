#include <Wire.h>
#include "controllerinfo.h"

#define DELAY 10

#define TO_BYTE_ARRAY(arr, val, bytes) for (int macro_i = 0; macro_i < bytes; macro_i++) arr[macro_i] = *((byte *)(val + macro_i));


bool used_addresses[MAX_PLAYERS];
byte arr[32]; //stores temporary information from get requests from players

/* I am the hub. */


void setup() {
  int i;
  Wire.begin();        // join i2c bus (address optional for master)
  Serial.begin(9600);  // start serial for output
  Serial.setTimeout(0.05);

  pinMode(8, OUTPUT);

  for (i = 0; i < MAX_PLAYERS; i++){
    used_addresses[i] = false;
  }

}

void loop() {
  int avail;  //available address for players
  
  Wire.requestFrom(DEFAULT_ADDRESS, 1); //if someone wants to join the game
  if (Wire.available()) {
    Wire.read();
    delay(DELAY);
    avail = get_next_available_address(used_addresses);

    Wire.beginTransmission(DEFAULT_ADDRESS);  //send them to next available address
    Wire.write(avail);
    Wire.endTransmission();
    delay(DELAY);

    used_addresses[avail] = true;
  }

  //request player number of player leaving the game/hub
  preparation_transmission(EXIT_ADDRESS, PREVIOUS_ADDRESS_FIELD, PREVIOUS_ADDRESS_SIZE);
  Wire.requestFrom(EXIT_ADDRESS, PREVIOUS_ADDRESS_SIZE);
  if (Wire.available()) { //prev_address_size is 1 byte, and always will be, so no need for while loop
    avail = Wire.read();
    delay(DELAY);

    exit_player(avail); //player exits hub

    preparation_transmission(EXIT_ADDRESS, DONE_FIELD, DONE_SIZE);  //send confirmation to exiting player they can disconnect
    Wire.beginTransmission(EXIT_ADDRESS);
    Wire.write('1');
    Wire.endTransmission();
    delay(DELAY);
  }

  //if message/command from game
  if (Serial.available()) {
    byte player;
    byte field;
    byte action;
    int i;
    int len;
    player = Serial.read();
    field = Serial.read();
    //first send field to be altered/requested. Then send 0 or 1 as a byte to represent get vs set. Then (in case of get) send the value to set to
    switch(field) {
      case HEALTH_FIELD:
        action = Serial.read(); // get (0) or set (1)?
        if (action) { //set
          //read in health value's bytes to set player's health to
          len = (int) Serial.read();  //read byte size of incoming data
          for (i = 0;i < len; i++) {
            arr[i] = Serial.read();
          }
          set_player_health(player, arr);
        }
        else { //get
          get_player_health(player); //stores information in global variable arr
          Serial.write(HEALTH_SIZE);  //write how many bytes info we are sending is
          Serial.write(arr, HEALTH_SIZE); //send info
        }
        break;
        
      case SKILLPOINTS_FIELD:
        action = Serial.read();
        if (action) {
          len = (int) Serial.read();
          for (i = 0; i < len; i++) {
            arr[i] = Serial.read();
          }
          set_player_skillpoints(player, arr);
        }
        else {
          get_player_skillpoints(player);
          Serial.write(SKILLPOINTS_SIZE);
          Serial.write(arr, SKILLPOINTS_SIZE);
        }
        break;

      case ITEMS_OBTAIN_FIELD:
        len = (int) Serial.read();
        for (i = 0; i < len; i++) {
          arr[i] = Serial.read();
        }
        player_obtain_item(player, arr);
         
        break;
 
      case ITEMS_LOSE_FIELD:
        len = (int) Serial.read();
        for (i = 0; i < len; i++) {
          arr[i] = Serial.read();
        }
        player_lose_item(player, arr);

        break;

      case ITEMS_LOOK_FIELD:
        action = Serial.read();
        if (action) {
          len = (int) Serial.read();
          for (i = 0; i < len; i++) {
            arr[i] = Serial.read();
          }
          set_player_items(player, arr);
        }
        else {
          get_player_items(player);
          Serial.write(ITEMS_LOOK_SIZE);
          Serial.write(arr, ITEMS_LOOK_SIZE);
        }
        break;

      case PLAYERNAME_FIELD:
        action = Serial.read();
        if (action) {
          len = (int) Serial.read(); //read byte size of incoming data
          for (i = 0; i < len; i++) {
            arr[i] = Serial.read();
          }
          set_player_name(player, arr, len);
        }
        else {
          i = get_player_name(player);
          Serial.write(i);
          Serial.write(arr, i);
        }
        break;

      case STATS_FIELD:
        action = Serial.read();
        if (action) {
          len = (int) Serial.read();
          for (i = 0; i < len; i++) {
            arr[i] = Serial.read();
          }
          set_player_stats(player, arr);
        }
        else {
          get_player_stats(player);
          Serial.write(STATS_SIZE);
          Serial.write(arr, STATS_SIZE);
        }
        
        break;

      case DONE_FIELD:
        preparation_transmission(player, DONE_FIELD, DONE_SIZE);
        Wire.beginTransmission(EXIT_ADDRESS);
        Wire.write('1');
        Wire.endTransmission();
        delay(DELAY);

        break;

      default:

        break;
    }
  }

}


void request_data_from_player(byte player, byte field_to_request, uint8_t data_size) {
  preparation_transmission(player, field_to_request, data_size);
  
  Wire.requestFrom(player, data_size);
}

void preparation_transmission(byte player, byte field, int data_size) {
  Wire.beginTransmission(player);
  Wire.write(field);
  Wire.write((byte) data_size);
  Wire.endTransmission();

  delay(DELAY);
}

void transmit_data_to_player(byte player, byte field_to_transmit, byte transmitted_value[], int data_size) {
  preparation_transmission(player, field_to_transmit, data_size);
  
  Wire.beginTransmission(player);
  Wire.write(transmitted_value, data_size);
  Wire.endTransmission();

  delay(DELAY);
}

void set_player_health(byte player, byte new_health_val[]) {
  transmit_data_to_player(player, HEALTH_FIELD, new_health_val, HEALTH_SIZE);
}

//stores player health in global variable arr
void get_player_health(byte player) {
  int i;

  request_data_from_player(player, HEALTH_FIELD, HEALTH_SIZE);
  
  for (i = 0; Wire.available(); i++){
    arr[i] = Wire.read();
  }
}

void set_player_skillpoints(byte player, byte new_skillpoints_val[]) {
  transmit_data_to_player(player, SKILLPOINTS_FIELD, new_skillpoints_val, SKILLPOINTS_SIZE);
}

//stores player skillpoints in global variable arr
void get_player_skillpoints(byte player) {
  int i;

  request_data_from_player(player, SKILLPOINTS_FIELD, SKILLPOINTS_SIZE);
  
  for (i = 0; Wire.available(); i++){
    arr[i] = Wire.read();
  }
}

void player_obtain_item(byte player, byte new_item[]) {
  transmit_data_to_player(player, ITEMS_OBTAIN_FIELD, new_item, ITEMS_OBTAIN_SIZE);
}


void player_lose_item(byte player, byte lost_item[]) {
  transmit_data_to_player(player, ITEMS_LOSE_FIELD, lost_item, ITEMS_LOSE_SIZE);
}

//stores player items in global variable arr
void get_player_items(byte player) {
  int i;
  
  request_data_from_player(player, ITEMS_LOOK_FIELD, ITEMS_OBTAIN_SIZE);

  for (i = 0; Wire.available(); i++) {
    arr[i] = Wire.read();
  }
}

void set_player_items(byte player, byte items[]) {
  transmit_data_to_player(player, ITEMS_LOOK_FIELD, items, ITEMS_OBTAIN_SIZE);
}

void set_player_name(byte player, byte new_name[], int name_len) {
  transmit_data_to_player(player, PLAYERNAME_FIELD, new_name, name_len);
}

//stores player name in global variable arr
int get_player_name(byte player) {
  int i;

  request_data_from_player(player, PLAYERNAME_FIELD, PLAYERNAME_MAX_SIZE);

  for (i = 0; Wire.available(); i++) {
    arr[i] = Wire.read();
  }
  return i;
}

void set_player_stats(byte player, byte stats_vals[]) {
  transmit_data_to_player(player, STATS_FIELD, stats_vals, STATS_SIZE);
}

//stores player stats in global variable arr
void get_player_stats(byte player) {
  int i;

  request_data_from_player(player, STATS_FIELD, STATS_SIZE);

  for (i = 0; Wire.available(); i++) {
    arr[i] = Wire.read();
  }
}

int get_next_available_address(bool used_addresses[]) {
  int i;
  for (i = 0; i < MAX_PLAYERS; i++) {
    if (!used_addresses[i]) {
      return i;
    }
  }
  return -1;
}

//player exiting the hub
void exit_player(int address) {
  //communicate w/ game to make sure all final writes/reads/transfers etc are good and player can disconnect now
  used_addresses[address] = false;
  
}
