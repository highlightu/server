# :high_brightness: LAJI : Auto Highlighting :arrow_forward: Web service


> &#9989; &#10102; We analyze your Twitch videos &#127916;

> &#9989; &#10103; We give you a list of highlights back &#128140;

> &#9989; &#10104; We take care of your values &#128142;


<!-- blank line -->
![demo gif](static/images/demo.gif)
<!-- blank line -->

[![Build Status](http://img.shields.io/travis/badges/badgerbadgerbadger.svg?style=flat-square)](https://travis-ci.org/badges/badgerbadgerbadger) [![Coverage Status](http://img.shields.io/coveralls/badges/badgerbadgerbadger.svg?style=flat-square)](https://coveralls.io/r/badges/badgerbadgerbadger) [![License](http://img.shields.io/:license-gpl-blue.svg?style=flat-square)](http://badges.gpl-license.org)


## Installation

**Requirements**

Python : 3.7.0 or later (3.6 may compatible)

Opencv-Python : 4.0.0 or later

Twitch-Chat-Downloader : 3.1.0 [referenc link](https://pypi.org/project/tcd/)

### Clone

- Clone this repo to your local machine using `https://github.com/laji-cau/LAJI-HIGHLIGHTING.git`

### Dockerizing

- Later on

### Setup

To install the current release for Ubuntu server.
```bash
sudo apt update
sudo apt install git python3-venv libsm6 libxext6 libxrender1 ffmpeg

git clone https://github.com/laji-cau/LAJI-HIGHLIGHTING
cd LAJI-HIGHLIGHTING/

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
#### *Try run LAJI-HIGHLIGHTING*
Add your public IP or DNS to allow hosts.
```bash
$ vim django_capstone/settings
```
```python
ALLOWED_HOSTS = [
    'ADD YOUR PUBLIC IP or DNS',
    'localhost',
    '127.0.0.1',
]
```

This service provides with google login.<br/>
So, you have to activate [GOOGLE+ API](https://console.developers.google.com/apis/api/plus.googleapis.com),
and to create [OAuth 2.0 Client](https://console.developers.google.com/apis/credentials) as a 'web application',
and get API Key/Secret
```bash
$ vim Bash_dir/envs.json
```
```python
{
  "GOOGLE_KEY": "YOUR API_KEY",
  "GOOGLE_SECRET": "YOUR API_SECRET"
}
```

```bash
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver 0.0.0.0:8080
```

Now, you can use LAJI-HIGHLIGHTING service

## Features

> :thumbsup: Chat analyze
>> `We download a chatlog of a given Twitch video URL.`

>> `We analyze it by scoring each time with labeled words.`

> :astonished: Face recognition
>> `We check resized frames in the video whether there are detected faces.`

>> `We use Residual Network model to get face expression percentages`

- Check out [Final Report](https://github.com/laji-cau/Capstone-Project-2019-Doc/blob/master/Documents/final_report.pdf)

## Usage

- Check out [Use-case scenario](https://github.com/laji-cau/Capstone-Project-2019-Doc/blob/master/Documents/team8_manual.pdf)
- This will help you use this service from beginning

## How to contribute

### Step 1

- **Option 1**
    - 🍴 Fork this repo!

- **Option 2**
    - 👯 Clone this repo to your local machine using `https://github.com/laji-cau/LAJI-HIGHLIGHTING`

### Step 2

- **HACK AWAY!** 🔨🔨🔨

### Step 3

- 🔃 Create a new pull request 

---

## Team

|**JISU AN**|**ZINU JEON**|**HYUNJAE LEE**|
| :---: |:---:| :---:|
| [![JISU AN](https://avatars1.githubusercontent.com/u/20200203?v=3&s=200)](http://github.com/ajs7270)    | [![ZINU JEON](https://avatars1.githubusercontent.com/u/20857275?v=3&s=200)](http://github.com/zinuzian) | [![HYUNJAE LEE](https://avatars1.githubusercontent.com/u/29877872?v=3&s=200)](http://github.com/hyunjae-lee) |
| <a href="http://github.com/ajs7270" target="_blank">`github.com/ajs7270`</a> | <a href="http://github.com/zinuzian" target="_blank">`github.com/zinuzian`</a> | <a href="http://github.com/hyunjae-lee" target="_blank">`github.com/hyunjae-lee`</a> |

---

## License

[![License](http://img.shields.io/:license-gpl-blue.svg?style=flat-square)](http://badges.gpl-license.org)

- **[GPL-3.0 license](https://opensource.org/licenses/gpl-license.php)**
- Copyright 2019 © LAJI
