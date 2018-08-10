/* THIS FILE HAS BEEN AUTOGENERATED BY FLORA-TOOLS */

#ifndef PROTOCOL_GLORIA_GLORIA_CONSTANTS_H_
#define PROTOCOL_GLORIA_GLORIA_CONSTANTS_H_

#include <stdint.h>

#define GLORIA_HEADER_LENGTH %%GLORIA_HEADER_LENGTH%%
#define GLORIA_ACK_LENGTH %%GLORIA_ACK_LENGTH%%
#define GLORIA_CLOCK_DRIFT %%GLORIA_CLOCK_DRIFT%% // +- %%GLORIA_CLOCK_DRIFT_PLUSMINUS%% ppm @ %%TIMER_FREQUENCY%%
#define GLORIA_BLACK_BOX_SYNC_DELAY %%GLORIA_BLACK_BOX_SYNC_DELAY%% // %%human_time(GLORIA_BLACK_BOX_SYNC_DELAY)%%
#define GLORIA_MAX_ACKS %%GLORIA_MAX_ACKS%%
#define GLORIA_RADIO_SLEEP_TIME %%GLORIA_RADIO_SLEEP_TIME%% // %%human_time(GLORIA_RADIO_SLEEP_TIME)%%
#define GLORIA_RADIO_WAKEUP_TIME %%GLORIA_RADIO_WAKEUP_TIME%% // %%human_time(GLORIA_RADIO_WAKEUP_TIME)%%
#define GLORIA_RADIO_WAKEUP_TIME_COLD 28000 // 3.5 ms
#define GLORIA_MAX_DRIFT 2 // 2 s

#define GLORIA_POWER_LEVELS 2

typedef struct {
	uint32_t slotOverhead;
	uint32_t slotAckOverhead;
	uint32_t floodInitOverhead;
	uint32_t floodFinishOverhead;
	uint32_t rxOffset;
	uint32_t rxTriggerDelay;
	uint32_t txTriggerDelay;
	uint32_t txSync;
	uint32_t rxSetup;
	uint32_t txSetup;
	uint16_t preambleTimeout;
    uint32_t mcuTimeout;
} gloria_timings_t;

extern gloria_timings_t gloria_timings[];

#endif /* PROTOCOL_GLORIA_GLORIA_CONSTANTS_H_ */
