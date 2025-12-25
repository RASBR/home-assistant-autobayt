# API Usage Guidelines

*See [docs/agent/050-api-response-samples.md](docs/agent/050-api-response-samples.md) for response sample.*

## IDs
- User ID to be provided when adding the integration to Home Assistant.
- Device, Location, and Room IDs will be provided as responses via APIs.

## GET

**URL:** https://api.autobayt.com/v1/user/get-things

Add the below to get related information:
* **User Devices:** `?user_id=` *user_id* - *Phase 1*
* **Device:** `?device_id=` *device_id* - *Phase 2*
* **User Devices:** `?loc_id=` *loc_id* - *Phase 2*
* **Room:** `?room_id=` *room_id* - *Phase 2*

## POST

See `docs/agent/050-api-response-samples.md` for response sample.

**URL**
https://api.autobayt.com/v1/device/trigger

---

##### **Headers**

Content-Type: application/json

##### **Authorization:**  *Optional (if required):*

Bearer <YOUR_TOKEN>


##### **Body**

Raw / JSON

```json
{
  "btnStates": [true],
  "btnIds": [0],
  "device_id": "485519ef8b1f"
}
```
##### **Command Line Example**

```bash
curl --location 'https://api.autobayt.com/v1/device/trigger' \
--header 'Content-Type: application/json' \
--data '{
  "btnStates": [true],
  "btnIds": [0],
  "device_id": "415919ef8b1f"
}'
```

## Notes

- IDs must be text
- btnStates and btnIds must be arrays
- device_id must be valid
- HTTPS is required
- Add Authorization header only if enforced by backend


