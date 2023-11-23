# Tiramisu REST API

The REST API is a beta feature that allows you to make modlog entries via REST requests.

You need to install aiohttp manually for this to work:
```
pip install aiohttp
```

Endpoint: `/modlog`
Method: `POST`
Accepts: `application/json`

#### Example JSON to post:

```json
{
    "instance_secret": "dcuEJ4FNBqTkhypQWP3xIxrzdeBKcBsP9NWAYaRNk_M",
    "guild_secret": "eNAk-pQY71vV-8fFDuyqDA",
    "guild_id": "604994115360391179",
    "action": "Banned",
    "user": "Notch",
    "uuid": "00000-00000-00000-00000",
    "platform": "Minecraft",
    "reason": "Being annoying",
    "duration": "2h",
    "notes": "Really. He was really annoying."

}
```
*All options are strings.*

###### Required
- `instance_secret`: The secret generated for the entire instance
- `guild_secret`: The secret for the current guild
- `guild_id`: The discord ID for the current guild
- `action`: What moderation action was performed
- `user`: The username for the user being acted upon
- `platform`: Which platform the action was performed on
- `reason`: Why this action was performed
- `author`: The username for the user who performed the action

###### Optional
- `duration`: The duration of this action
- `notes`: additional information about this action
