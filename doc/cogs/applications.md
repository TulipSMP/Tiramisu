# applications.py
A system for creating applications. When an application is made, it is sent to the `application_channel` with all the info the user has filled out, the user's name, tag and ID, etc.

## Slash Commands
### `/apply`
Apply for a position.

#### Options
* `age_group`: a `SlashOption` with `choices`, which age group does the user belong to?
* `reason`: a `str`, why should the user be accepted?
* `experience`: a `bool`, has the user been a moderator before?
* `position`: an optional `str`, what position is the user applying for?
