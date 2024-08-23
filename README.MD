# Features
- Read the value from Sharepoint list
- Set checkin date, checkout date, hotelname
- Update the value to the Sharepoint list

# Installation
### Create env
`py -3 -m venv .venv`
### Activate env
`.venv\Scripts\activate`
### Install requirement
`pip install requirement.txt`
### Run
`py run.py`

## Routes
- GET: /reservation/
- GET: /reservation/\<accountnumber\>
- PUT: /reservation/\<accountnumber\> without body or with body\
`{"checkin": "2024-08-17T12:42:43Z", "checkout": "2024-08-22T12:42:43Z"}`\
Optional:
  - checkin: %Y-%m-%dT%H:%M:%SZ
  - checkout: %Y-%m-%dT%H:%M:%SZ
  - hotelname: string

# Deploy to Production

## Change /src/__init__.py >> logging.basicConfig
- If local, change to\
`logging.basicConfig(filename=os.path.abspath("app.log"), level=logging.DEBUG)`
- If Docker,change to\
`logging.basicConfig(filename="/var/www/rsvdemo/app.log", level=logging.DEBUG)`

## Change run.py >> app.run
- If local, change to\
`app.run(host='127.0.0.1', port=8045, debug=True)`
- If Docker, change to\
`app.run(host='0.0.0.0')`

## Docker ENV
- Copy the package to the `/opt/rsvdemo/`
- Build image from scratch and Run docker Container\
`docker-compose up --build`
- Run Container if the Image is exist\
`docker-compose up --no-build`
- Deploy update changes by downloading the package from GitHub, or try `git pull`
- Once downloaded `unzip` the package
- Copy to the `/opt/rsvdemo/`
