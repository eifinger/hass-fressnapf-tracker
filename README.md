# fressnapf_tracker

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)
[![License][license-shield]](LICENSE.md)

![Project Maintenance][maintenance-shield]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Community Forum][forum-shield]][forum]

_Homeassistant Custom Component for [https://my.fressnapf_tracker.com/](https://my.fressnapf_tracker.com/)._

**This component will set up the following platforms.**

Platform | Description
-- | --
`binary_sensor` | Adds sensors to show the connection status of your trackers.
`button` | Shortcuts to service. Activate Super Live Mode, Ring, Vibrate and Request a Location Update.
`device_tracker` | Adds your trackers as device_trackers so they appear on the map.
`select` | Select the update interval.
`sensor` | Adds sensors like signal and battery strength of your trackers.

![example][exampleimg]
![configuration][configurationimg]

## Services

### weeenct.set_update_interval

Set the tracker update interval.

Name | Description | Example
-- | -- | --
`update_interval` | `The update interval. Possible values are 30S 1M 5M 10M 30M 1H.` | `30M`

### weeenct.activate_super_live

Activate the super live mode.

### weeenct.refresh_location

Request a location update.

### weeenct.ring

Let the tracker ring.

### weeenct.vibrate

Let the tracker vibrate.

## Installation

### HACS

The easiest way to add this to your Homeassistant installation is using [HACS](https://hacs.xyz/).

### Manual

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `fressnapf_tracker`.
4. Download _all_ the files from the `custom_components/fressnapf_tracker/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Blueprint"

Using your HA configuration directory (folder) as a starting point you should now also have this:

```text
custom_components/fressnapf_tracker/__init__.py
custom_components/fressnapf_tracker/button.py
custom_components/fressnapf_tracker/binary_sensor.py
custom_components/fressnapf_tracker/config_flow.py
custom_components/fressnapf_tracker/const.py
custom_components/fressnapf_tracker/device_tracker.py
custom_components/fressnapf_tracker/entity.py
custom_components/fressnapf_tracker/manifest.json
custom_components/fressnapf_tracker/select.py
custom_components/fressnapf_tracker/sensor.py
custom_components/fressnapf_tracker/services.py
custom_components/fressnapf_tracker/services.yaml
custom_components/fressnapf_tracker/translations/en.json
```

## Automations

I have configured the following two automations to save battery on the tracker without having it to turn on/off by hand:

```yaml
---
automation:
  - id: 743b7e7d-ffa8-4fa3-9c1c-62d9ada9ced8
    alias: "Setze Nayas Tracker Updaterate auf 1M wenn wir unterwegs sind"
    description: "Set Nayas tracker update rate to 1m when we are not at home"
    mode: single
    initial_state: true
    trigger:
      - platform: state
        entity_id: input_boolean.is_home
        from: "on"
        to: "off"
    action:
      - service: fressnapf_tracker.set_update_interval
        target:
            entity_id: device_tracker.naya
        data:
          update_interval: "1M"
  - id: 652b4b69-c951-4861-8b7d-3cbb15fc8b79
    alias: "Setze Nayas Tracker Updaterate auf 60M wenn wir zu Hause sind"
    description: "Set Nayas tracker update rate to 60m when we are at home"
    mode: single
    initial_state: true
    trigger:
      - platform: state
        entity_id: input_boolean.is_home
        from: "off"
        to: "on"
    action:
      - service: fressnapf_tracker.set_update_interval
        target:
          entity_id: device_tracker.naya
        data:
          update_interval: "60M"
````


<a href="https://www.buymeacoffee.com/eifinger" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/black_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a><br>

[buymecoffee]: https://www.buymeacoffee.com/eifinger
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/eifinger/hass-fressnapf_tracker?style=for-the-badge
[commits]: https://github.com/eifinger/hass-fressnapf_tracker/commits/main
[exampleimg]: https://github.com/eifinger/hass-fressnapf_tracker/blob/main/example.png?raw=true
[configurationimg]: https://github.com/eifinger/hass-fressnapf_tracker/blob/main/configuration.png?raw=true
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/t/custom-integration-fressnapf_tracker/300996
[license-shield]: https://img.shields.io/github/license/eifinger/hass-fressnapf_tracker.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Kevin%20Stillhammer%20%40eifinger-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/eifinger/hass-fressnapf_tracker.svg?style=for-the-badge
[releases]: https://github.com/eifinger/hass-fressnapf_tracker/releases
