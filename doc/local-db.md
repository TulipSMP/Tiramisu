# Storing DB-related values as yml
Is available in `config/config.yml`. It can be set via the below yaml:
```yaml
storage:
  db: False
```
**HOWEVER:** this setting is NOT reccomended for ANYONE. It is for developers being able to test cogs and other changes that do not require a database. It _could_ be used by a small discord group self-hosting the bot soley for their personal use, but we do not warranty this (because [we dont warranty anything](../LICENSE))