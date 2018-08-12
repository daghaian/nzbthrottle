# nzbthrottle


## Description
Nzbthrottle was designed in order to dynamically control the bandwidth allocation when users are actively streaming from Plex to avoid unnecessary buffering while still allowing the user to download at the fastest rate possible.

## Installation

*Note: Must have Python 3.5 or higher*

1. Run ```pip install -r requirements.txt``` from within the project root
2. Copy ```config_example.json``` and name the new file ```config.json```
3. Edit the config with all of your appropriate credentials

***Sample Config:***

```json
{
  "plex":
  {
    "url":"http://localhost:32400",
    "interval":60,
    "token": "daf32j3ik3l2k"
  },
  "nzbget":
  {
    "username":"test_user",
    "password":"test_pass",
    "url":"http://localhost:6789",
    "speeds":{
      "1":5000,
      "2":4000,
      "3":3000,
      "4":2000,
      "5":1000
    }
  }
}
```

***Plex***

```url``` - URL of your Plex Server

```interval``` - Interval with which to check for active streams (seconds)

```token``` - Your X-Plex-Token

***Nzbget***

```username``` - Username for Nzbget

```password``` - Password for Nzbget

```url``` - URL of your NZBGet Client

```speeds``` - Define speed to throttle to (in kB/s) based on number of active streams

## Usage

```python throttle.py [-h] [--log-level=['DEBUG','INFO','WARN']]```

