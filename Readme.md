# Sonarr Archiver

This container builds upon the `alekslyse/sonarr_tag_move` project

The script has been extended to support **multiple tag/root-folder pairs**.  
To use this feature, define one or more `TAG_FOLDER_PAIR_X` environment variables, e.g.:


    TAG_FOLDER_PAIR_1=archive:/archive/tvshows
    TAG_FOLDER_PAIR_2=running:/tvshows

There is no fixed limit to the number of pairs, as long as the variables are named sequentially (without gaps).

Processing is scheduled via a **cron expression** and starts 30 seconds after container startup.

> 🐳 Pull the image from: `docker.io/buesche87/sonarrchiver`

## Environment

| variable | value | explanation |
| ----------- | ----------- | ----------- |
| `SONARR_API_URL` | `http://sonarr:8989/api/v3` | Sonarr API endpoint |
| `SONARR_API_KEY` | `d5198e8de5259712b6361a56de515a51` | Sonarr API key |
| `CRON_SCHEDULE` | `0 0 * * *` | Cron schedule for processing |
| `LOG_LEVEL` | `INFO` | Log level (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |
| `TEST_SERIES_TITLE` | `Andor` | Keep empty to process all series |
| `TAG_FOLDER_PAIR_1` | `archive:/archive/tvshows` | Tag and root folder (must exist in Sonarr) |
| `TAG_FOLDER_PAIR_2` | `running:/tvshows` | Tag and root folder (must exist in Sonarr) |

