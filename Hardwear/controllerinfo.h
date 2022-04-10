#include <Wire.h>

#define EXIT_BUTTON_PIN 10

#define DEFAULT_ADDRESS 0x7f
#define EXIT_ADDRESS 0x7e

#define HEALTH_FIELD 0x0
#define SKILLPOINTS_FIELD 0x1
#define ITEMS_OBTAIN_FIELD 0x2
#define ITEMS_LOSE_FIELD 0x3
#define ITEMS_LOOK_FIELD 0x4
#define PLAYERNAME_FIELD 0x5
#define STATS_FIELD 0x6
#define PREVIOUS_ADDRESS_FIELD 0x7
#define DONE_FIELD 0x8

#define HEALTH_SIZE 0x2
#define SKILLPOINTS_SIZE 0x2
#define ITEMS_OBTAIN_SIZE 0x2
#define ITEMS_LOSE_SIZE 0x2
#define ITEMS_LOOK_SIZE 0x2
#define PLAYERNAME_MAX_SIZE 0x10
#define STATS_SIZE 0x6
#define PREVIOUS_ADDRESS_SIZE 0x1
#define DONE_SIZE 0x1

#define READ_INT() Wire.read() + (Wire.read() << 8)

typedef struct stats {
    int max_health;
    int attack;
    int defense;
} Stats;

typedef struct player {
  int health;
  int skillpoints;
  int items;
  uint8_t playername[16];
  Stats stats;
} Player;