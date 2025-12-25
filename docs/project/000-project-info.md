# 000 — Project Info

## Project Name
**AUTOBAYT**

**Autobayt** is a Jordanian manufacturer of IoT smart devices. currently it has one line of devices which is smart switches that comes in 3 different models as follows:

* **Single**
  Has *one* single switch
* **Double**
  Has *two* switches
* **Triple**
  Has *three* switches

## Purpose
- AUTOBAYT is a Home Assistant integration.  
- It provides tools for controlling devices and reading their information,from an Autobayt account.  
- The project is designed to run a Home Assistant integration.

## Scope
Project starts at Phase 1, following phases fix bugs and may introduce feature
- The integration handles
  - **Account** → user account related information (sensors) if any. *Phase 3 and above*
  - **Devices** → Controlling devices and reading their sensors data/statuses. *Phase 1*

- Extensible: additional sensors/

## Technology Stack
- **Backend**: Python 3.12+
- **Database**: Handled by Home Assistant.
- **Frontend**: Handled by Home Assistant.
- **Setup/Deployment**: Manual *Phase 1* and via **HACS** *Phase 3*.
- **Version Control**: GitHub [home-assistant-autobayt](https://github.com/RASBR/home-assistant-autobayt.git)

## Audience
Home Assistant users who have Autobayt products installed in their environments.


## Notes for AI Agent
- Keep code simple, explicit, and easy to maintain.
- Follow project conventions defined in `030-conventions.md`.
- Do not introduce features, modules, or integrations not requested.

