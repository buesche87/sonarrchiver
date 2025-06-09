# Sonarr Archiver

This container builds upon the `alekslyse/sonarr_tag_move` project 

Pull the image from `docker.io/buesche87/sonarrchiver`

## Environment

| variable | value | explanation |
| ----------- | ----------- | ----------- |
| SONARR_API_URL | `http://sonarr:8989/api/v3` | sonarr api endpoint |
| SONARR_API_KEY | `d5198e8de5259712b6361a56de515a51` | sonarr api key |
| TAG_NAME | `archive` | tag to process |
| NEW_ROOT_FOLDER | `/archive/tvshows` | root folder (must exist in sonarr) |
| CRON_SCHEDULE | `0 0 * * *` | processing schedule |
| TEST_SERIES_TITLE | `Andor` | keep empty to process all series |


> Processing starts 3 minutes after container start and on schedule
