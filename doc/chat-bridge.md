# Chat Bridge System

## JSON
This is the base format of json sent over the webhook:

```json
# Outgoing from Tiramisu
{
    "origin": "discord", # The only messages the client will recieve will be from origin discord. you should not check this value
    "author": {
        "name": "Display Name", # User's discord display name
        "username": "user.name", # User's discord username
        "id": 00000000000000, # User's discord ID
        "profile": "https://cdn.discordapp.com/profiles/users-profile-pic-url.jpeg" # URL to their profile
    },
    "message": {
        "content": "Heyyo <@705150784941064293>, this is the message im sending!", # The content of their message
        "content_clean": "Heyyo @Krafter, this is the message im sending!", # The content of their message, with mentions cleaned.
        "attachments": ["https://cdn.discordapp.com/image.png"], # A list of URLs to any attachments
        "timestamp": 1087787882242 # Timestamp of message send in unix millis
    },
    "meta": {
        "response": 200, # HTTP Response Code
        "message": "Ok" # Other info
    }
}

# Incoming from external bridge
{
    "origin": "external",
    "author": {
        "name": "Display Name", # User's name
        "username": "user.name", # User's unique username
        "id": 00000000000000, # User's unique ID of some kind
        "profile": "https://cdn.namemc.com/profiles/users-profile-pic-url.jpeg" # URL to their profile
    },
    "message": {
        "content": "Heyyo, this is the message im sending!", # The content of their message
        "attachments": ["https://cdn.discordapp.com/image.png"], # A list of URLs to any attachments
        "timestamp": 1087787882259 # Timestamp of message send in unix millis
    },
    "authority": {
        "uuid": "0000-00000000-fffff-000000", # UUID of bridge
        "guild": 9038245903258043, # Numerical ID of discord destination guild
        "channel": 323827483925894, # Numerical ID of discord destination channel
    }
}

# Internal 
{
    "origin": "internal",
    "author": {
        "name": "Display Name", # User's discord display name
        "username": "user.name", # User's discord username
        "id": 00000000000000, # User's discord ID
        "profile": "https://cdn.discordapp.com/profiles/users-profile-pic-url.jpeg" # URL to their profile
    },
    "message": {
        "content": "Heyyo, this is the message im sending!", # The content of their message
        "attachments": ["https://cdn.discordapp.com/image.png"], # A list of URLs to any attachments
        "timestamp": 1087787882242 # Timestamp of message send in unix millis
    },
    "authority": {
        "uuid": "00000-000000-00000-0000", # Internal UUID
        "guild": 38927598437954435, # Numerical ID of discord guild it was in
        "channel": 3897485902375984, # Numerical ID of discord channel it was in
    }
}
```