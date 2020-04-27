# Visual MOT 

Visual MOT is a Web Application that retrieves vehicle data from the [DVLA](https://vehicleenquiry.service.gov.uk/) by using an image, either of an existing one using a desktop or taking one on a smartphone.

### Built With
* [Bootstrap](https://getbootstrap.com)
* [JQuery](https://jquery.com)
* [Flask](https://palletsprojects.com/p/flask/)

## Prerequisites

Before you begin, ensure you have met the following requirements:
<!--- These are just example requirements. Add, duplicate or remove as required --->
* You have `Python 3`.
* You are using a `Windows or Linux`.
* Get a free API Key at [OpenALPR](https://cloud.openalpr.com/account/register) and enter in `secrect_key.txt`
* You have [Java](https://www.oracle.com/java/technologies/javase-downloads.html)
* You have Google Chrome and corresponding chromedriver [Chromedrivers](https://chromedriver.chromium.org/downloads)

## Live Version 
[Visualmot](https://visualmot.app)

## Installation

1. Clone repository
```
git clone https://github.com/Adam-94/Individual-Project.git
```

**Ubuntu 20.04**

**Virtual Environment Setup**

1. Install virtual environment
```
sudo apt install -y python3-venv
```

2. Create virtual environment
```
python3 -m venv env
```

3. Activate virtual environment
```
source env/bin/activate
```

4. install requirements
```
pip3 install -r requirements.txt
```

### Windows

**Virtual Environment Setup**

1. Install virtual environment
```
pip install virutalenv
```

2. Create virtual environment
```
virutalenv env
```

3. Activate virtual environment
```
env\Scripts\activate
```

4. Install requirements
```
pip install -r requirements.txt
```

## Usage

1. Normal usage
```
python main.py
```

2. Use on other devices with IPv4 Address
```
Example: http://192.168.0.34:5000/
```

<!-- LICENSE -->
## License

Distributed under the MIT License. See [LICENSE](https://github.com/Adam-94/Individual-Project/blob/master/LICENSE) for more information.


