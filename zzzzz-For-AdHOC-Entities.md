# GET/POST Methods Sample Responses

** IDS are Scrambled as the below data is meant to be a sample**

## User GET method

**URL:** https://api.autobayt.com/v1/user/get-things?user_id=67b1b9cbc53b260012fe10f6

**Response**
```json
[
  {
    "room_id": "67b1b9cbc53b260012fe10f7",
    "connection_status": true,
    "slave_id": "",
    "is_hub": true,
    "is_updating": false,
    "perc": 0,
    "period": 20000,
    "pat_period": 30,
    "device_id": "485519ef1eb1",
    "name": "Entrance",
    "firmware_version": "1.9.11",
    "model_name": "SW100HV1",
    "sstr": "-67",
    "loc_id": "67b1b9e1c53b260012fe10f9",
    "next_firmware": [
      {
        "version_name": "1.9.11",
        "file_name": "sw100hv1_1.9.11.bin",
        "version_code": 92,
        "require_client_update": false,
        "app_version_code": 1
      }
    ],
    "buttons": [
      {
        "switch_state": false,
        "dpb_state": 0,
        "power_on_state": "Same",
        "mode": 0,
        "toggle_delay": 0,
        "name": "SW100HV1",
        "button_id": 0
      }
    ],
    "room_name": "default"
  },
  {
    "room_id": "67b1b9cbc53b260012fe10f7",
    "connection_status": true,
    "slave_id": "",
    "is_hub": true,
    "is_updating": false,
    "perc": 0,
    "period": 20000,
    "pat_period": 30,
    "device_id": "485519ef2b44",
    "name": "Stairs-GF",
    "firmware_version": "1.9.11",
    "model_name": "SW100HV1",
    "sstr": "-70",
    "loc_id": "67b1b9e1c53b260012fe10f9",
    "next_firmware": [
      {
        "version_name": "1.9.11",
        "file_name": "sw100hv1_1.9.11.bin",
        "version_code": 92,
        "require_client_update": false,
        "app_version_code": 1
      }
    ],
    "buttons": [
      {
        "switch_state": false,
        "dpb_state": 0,
        "power_on_state": "Off",
        "mode": 0,
        "toggle_delay": 0,
        "name": "SW100HV1",
        "button_id": 0
      }
    ],
    "room_name": "default"
  },
  {
    "room_id": "67b1b9cbc53b260012fe10f7",
    "connection_status": false,
    "slave_id": "485519ef1eb1",
    "is_hub": false,
    "is_updating": false,
    "perc": 0,
    "period": 20000,
    "pat_period": 30,
    "device_id": "485519ef181a",
    "name": "Stairs-FF",
    "firmware_version": "1.9.7",
    "model_name": "SW100HV1",
    "sstr": "-54",
    "loc_id": "67b1b9e1c53b260012fe10f9",
    "next_firmware": [
      {
        "version_name": "1.9.11",
        "file_name": "sw100hv1_1.9.11.bin",
        "version_code": 92,
        "require_client_update": false,
        "app_version_code": 1
      }
    ],
    "buttons": [
      {
        "switch_state": false,
        "dpb_state": 0,
        "power_on_state": "On",
        "mode": 0,
        "toggle_delay": 0,
        "name": "Button 1",
        "button_id": 0
      }
    ],
    "room_name": "default"
  },
  {
    "room_id": "67b1b9cbc53b260012fe10f7",
    "connection_status": true,
    "slave_id": "",
    "is_hub": true,
    "is_updating": false,
    "perc": 0,
    "period": 20000,
    "pat_period": 30,
    "device_id": "d8bc388791d2",
    "name": "IT Center Light",
    "firmware_version": "1.9.9",
    "model_name": "SW100PMV1",
    "sstr": "-87",
    "loc_id": "67b1b9e1c53b260012fe10f9",
    "next_firmware": [
      {
        "version_name": "1.9.10",
        "file_name": "sw100pmv1_1.9.10.bin",
        "version_code": 64,
        "require_client_update": false,
        "app_version_code": 1
      }
    ],
    "buttons": [
      {
        "switch_state": false,
        "dpb_state": 0,
        "power_on_state": "Off",
        "mode": 0,
        "toggle_delay": 0,
        "name": "SW100PMV1",
        "button_id": 0
      }
    ],
    "room_name": "default"
  },
  {
    "room_id": "67b1b9cbc53b260012fe10f7",
    "connection_status": true,
    "slave_id": "",
    "is_hub": true,
    "is_updating": false,
    "perc": 0,
    "period": 20000,
    "pat_period": 30,
    "device_id": "341876rt9sm3",
    "name": "Pumps Room",
    "firmware_version": "1.9.11",
    "model_name": "SW200LV1",
    "sstr": "-49",
    "loc_id": "p7k3m9dex8nb450036re84t2",
    "next_firmware": [
      {
        "version_name": "1.9.11",
        "file_name": "sw200lv1_1.9.11.bin",
        "version_code": 47,
        "require_client_update": false,
        "app_version_code": 1
      }
    ],
    "buttons": [
      {
        "switch_state": false,
        "dpb_state": 0,
        "power_on_state": "Off",
        "mode": 0,
        "toggle_delay": 0,
        "name": "Inside",
        "button_id": 0
      },
      {
        "switch_state": false,
        "dpb_state": 0,
        "power_on_state": "Off",
        "mode": 0,
        "toggle_delay": 0,
        "name": "Outside",
        "button_id": 1
      }
    ],
    "room_name": "default"
  },
  {
    "room_id": "67b1b9cbc53b260012fe10f7",
    "connection_status": false,
    "slave_id": "",
    "is_hub": true,
    "is_updating": false,
    "perc": 0,
    "period": 20000,
    "pat_period": 30,
    "device_id": "485519e621ae",
    "name": "Extractor",
    "firmware_version": "1.9.9",
    "model_name": "SW100PMV1",
    "sstr": "-50",
    "loc_id": "67b1b9e1c53b260012fe10f9",
    "next_firmware": [
      {
        "version_name": "1.9.10",
        "file_name": "sw100pmv1_1.9.10.bin",
        "version_code": 64,
        "require_client_update": false,
        "app_version_code": 1
      }
    ],
    "buttons": [
      {
        "switch_state": false,
        "dpb_state": 0,
        "power_on_state": "Off",
        "mode": 0,
        "toggle_delay": 0,
        "name": "Extractor",
        "button_id": 0
      }
    ],
    "room_name": "default"
  },
  {
    "room_id": "67b1b9cbc53b260012fe10f7",
    "connection_status": true,
    "slave_id": "485519ef8b1f",
    "is_hub": false,
    "is_updating": false,
    "perc": 0,
    "period": 20000,
    "pat_period": 30,
    "device_id": "d8bc3886db74",
    "name": "P EX",
    "firmware_version": "1.9.11",
    "model_name": "SW300LV1",
    "sstr": "-53",
    "loc_id": "67b1b9e1c53b260012fe10f9",
    "next_firmware": [
      {
        "version_name": "1.9.11",
        "file_name": "sw300lv1_1.9.11.bin",
        "version_code": 56,
        "require_client_update": false,
        "app_version_code": 1
      }
    ],
    "buttons": [
      {
        "switch_state": true,
        "dpb_state": 0,
        "power_on_state": "Off",
        "mode": 0,
        "toggle_delay": 0,
        "name": "EX",
        "button_id": 0
      },
      {
        "switch_state": false,
        "dpb_state": 0,
        "power_on_state": "Off",
        "mode": 0,
        "toggle_delay": 0,
        "name": "Button 2",
        "button_id": 1
      },
      {
        "switch_state": false,
        "dpb_state": 0,
        "power_on_state": "Off",
        "mode": 0,
        "toggle_delay": 0,
        "name": "Button 3",
        "button_id": 2
      }
    ],
    "room_name": "default"
  }
]
```

## Device GET method

**URL:** https://api.autobayt.com/v1/device/get-things?device_id=485519ef8b1f

**Response**
```json
[
  {
    "room_id": "67b1b9cbc53b260012fe10f7",
    "connection_status": true,
    "slave_id": "",
    "is_hub": true,
    "is_updating": false,
    "perc": 0,
    "period": 20000,
    "pat_period": 30,
    "device_id": "485519ef8b1f",
    "name": "Pumps Room",
    "firmware_version": "1.9.11",
    "model_name": "SW200LV1",
    "sstr": "-49",
    "loc_id": "67b1b9e1c53b260012fe10f9",
    "next_firmware": [
      {
        "version_name": "1.9.11",
        "file_name": "sw200lv1_1.9.11.bin",
        "version_code": 47,
        "require_client_update": false,
        "app_version_code": 1
      }
    ],
    "buttons": [
      {
        "switch_state": false,
        "dpb_state": 0,
        "power_on_state": "Off",
        "mode": 0,
        "toggle_delay": 0,
        "name": "Inside",
        "button_id": 0
      },
      {
        "switch_state": false,
        "dpb_state": 0,
        "power_on_state": "Off",
        "mode": 0,
        "toggle_delay": 0,
        "name": "Outside",
        "button_id": 1
      }
    ]
]
```

## SWITCH On/Off POST method

```bash
curl --location 'api.autobayt.com/v1/device/trigger' \ --header 'Content-Type: application/json' \ --data '{ "btnStates": [true], "btnIds": [0], "device_id": "485519ef8b1f"
```

**Response**
```json
{
  "device": {
    "_id": "68f749c5a211ac001359119b",
    "room_id": "67b1b9cbc53b260012fe10f7",
    "connection_status": true,
    "device_status": "conf_done",
    "slave_id": "",
    "is_hub": true,
    "is_updating": false,
    "perc": 0,
    "period": 20000,
    "pat_period": 30,
    "on_gogl": false,
    "on_alexa": false,
    "device_id": "485519ef8b1f",
    "name": "Pumps Room",
    "model_code": "sw200lv1",
    "firmware_version": "1.9.11",
    "model_name": "SW200LV1",
    "sstr": "-49",
    "updated": "2025-10-21T08:52:21.616Z",
    "__v": 0,
    "loc_id": "67b1b9e1c53b260012fe10f9",
    "user_id": "67b1b9cbc53b260012fe10f6",
    "added_by": "67b1b9cbc53b260012fe10f6",
    "connected": "2025-12-23T04:34:30.742Z",
    "ram": "34776"
  }
}
```





