/* THIS FILE HAS BEEN AUTOGENERATED BY FLORA-TOOLS */

#include <radio_constants.h>

const radio_config_t radio_modulations[] =
{
        <%- for config in configurations %>
		    {   // %%loop.index - 1%%
		        .modem = %%config.modem%%,
		        .bandwidth = %%config.bandwidth%%,
		        .datarate = %%config.datarate%%,
		        <%- if config.coderate %>
		        .coderate = %%config.coderate%%,
		        <%- else %>
		        .fdev = %%config.fdev%%,
		        <%- endif %>
		        .preambleLen = %%config.preamble_len%%,
		    },
		<%- endfor %>
};

#ifndef US915
const radio_band_t radio_bands[] =
{
		<%- for band in bands %>
		    { .centerFrequency = %%band.center_frequency%%, .bandwidth = %%band.bandwidth%%, .dutyCycle = %%band.duty_cycle%%, .maxPower = %%band.max_power%% }, // %%loop.index - 1%%
		<%- endfor %>
};

const radio_band_group_t lora_band_groups[] = {
		<%- for band_group in band_groups %>
		    { .lower = %%band_group.lower%%, .upper = %%band_group.upper%% },
		<%- endfor %>
};

#else
const lora_band_t radio_bands[] =
{
		<%- for band in bands_us915 %>
		    { .centerFrequency = %%band.center_frequency%%, .bandwidth = %%band.bandwidth%%, .dutyCycle = %%band.duty_cycle%%, .maxPower = %%band.max_power%% }, // %%loop.index - 1%%
		<%- endfor %>
};

const radio_band_group_t radio_band_groups[] = {
		<%- for band_group in band_groups_us915 %>
		    { .lower = %%band_group.lower%%, .upper = %%band_group.upper%% },
		<%- endfor %>
};

#endif

const radio_cad_params_t radio_cad_params[] = {
		{.symb_num = LORA_CAD_01_SYMBOL, .cad_det_peak = 25, .cad_det_min = 10}, // SF12
		{.symb_num = LORA_CAD_01_SYMBOL, .cad_det_peak = 24, .cad_det_min = 10}, // SF11
		{.symb_num = LORA_CAD_01_SYMBOL, .cad_det_peak = 23, .cad_det_min = 10}, // SF10
		{.symb_num = LORA_CAD_01_SYMBOL, .cad_det_peak = 22, .cad_det_min = 10}, // SF9
		{.symb_num = LORA_CAD_01_SYMBOL, .cad_det_peak = 21, .cad_det_min = 10}, // SF8
		{.symb_num = LORA_CAD_01_SYMBOL, .cad_det_peak = 20, .cad_det_min = 10}, // SF7
		{.symb_num = LORA_CAD_01_SYMBOL, .cad_det_peak = 19, .cad_det_min = 10}, // SF6
		{.symb_num = LORA_CAD_01_SYMBOL, .cad_det_peak = 18, .cad_det_min = 10}, // SF5
};

const uint32_t radio_toas[][256] =
{
        <%- for modulation_toa in radio_toas %>
		    {   // %%loop.index - 1%%
		        <%- for payload_toa in modulation_toa %>
		            %%payload_toa%%, // %%loop.index - 1%%: %%human_time(payload_toa)%%
		        <%- endfor %>
		    },
		<%- endfor %>
};