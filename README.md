# Binge watch
Amazon lambda for recommending what tv show to watch next.
This lambda supports the Binge watch Alexa custom skill.

The user can:
- setup new shows
- reset all setups
- ask for a show recommendation (random selection)

Trakt API is used to search for related shows when setting up a new show.
DynamoDB is used to store user profiles.
