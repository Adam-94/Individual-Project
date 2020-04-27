from flask import Flask, request, redirect, render_template
from flask import jsonify, Response, session
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import base64
import json
import requests
import cv2

app = Flask(__name__)

IMAGE_PATH = 'static/images/test.jpg'
KEY_PATH = 'secret_key.txt'

@app.route('/')
def index():
     return render_template('index.html')

@app.route('/take_pic', methods=["POST"])
def get_image():
    if request.method == "POST":
        print("Incoming...")
        if 'image' not in request.files:
            return redirect(request.url)
        try:
            if 'image' in request.files:
                imageFile = request.files['image']
                print(imageFile)
                with Image.open(imageFile) as img:
                    img.save(IMAGE_PATH)
                print("Image saved!")
                fix_image_orientation()
        except Exception as e:
            print(e)
        return jsonify('Ok')


@app.route('/')
def fix_image_orientation():
    img = cv2.imread(IMAGE_PATH)

    out = cv2.transpose(img)
    out = cv2.flip(out,flipCode=0)

    out = cv2.transpose(img)
    out = cv2.flip(out,flipCode=1)

    cv2.imwrite(IMAGE_PATH, out)

    print('rotated!')



def click_user_input(car_data = {}):

    #Remove options to disable headless Chrome
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--no-extensions')
    options.add_argument('--headless')

    print("Car data before dvla: ", car_data)

    selector = ['#wizard_vehicle_enquiry_capture_vrn_vrn',
            '#yes-vehicle-confirm',
            '#capture_confirm_button',
            'div.govuk-grid-column-one-half:nth-child(1) > div:nth-child(1)',
            '#mot-status-panel',
            '#make > dd:nth-child(2)',
            '#year_of_manufacture > dd:nth-child(2)']

    print("Getting all car data...")
    try:
        #Remove options to disable headless
        driver = webdriver.Chrome(options=options)
        driver.get('https://vehicleenquiry.service.gov.uk/')
        print(driver.current_url)

        # Enter vehicle's number plate and submit
        driver.implicitly_wait(10)
        inputElement = driver.find_element_by_css_selector(selector[0])
        inputElement.send_keys(car_data['plate'])
        inputElement.send_keys(Keys.ENTER)
        print("Entered Numplate")
        driver.implicitly_wait(10)

	# Confirm vehicle check
        inputElement = driver.find_element_by_css_selector(selector[1]).click()
        inputElement = driver.find_element_by_css_selector(selector[2]).click()

	# Retrieve Tax status
        inputElement = driver.find_element_by_css_selector(selector[3])
        car_data['tax'] = inputElement.text

        # Retrieve MOT status
        inputElement = driver.find_element_by_css_selector(selector[4])
        car_data['mot'] = inputElement.text

	# Grab the car make
        inputElement = driver.find_element_by_css_selector(selector[5])
        car_data['car'] = inputElement.text

	# Grab the year of manufacture for vehicle
        inputElement = driver.find_element_by_css_selector(selector[6])
        car_data['year'] = inputElement.text
    finally:
        driver.close()
        driver.quit()
    return car_data



def get_user_data():
    car_data = {
        "plate": "",
        "car": "",
        "year": "",
        "tax": "",
        "mot": ""
    }

    print("Getting number plate!")
    car_data['plate'] = extract_numberplate()

    if car_data['plate'] != "Plate not found!":
        click_user_input(car_data)
    else:
        print("No plate found")
        car_data['car'] = ""
        car_data['year'] = ""
        car_data['tax'] = ""
        car_data['mot'] = ""

    print("Got all car data: ", car_data)
    return car_data



@app.route('/motdata', methods=['GET'])
def pass_data():
    car_data = get_user_data()
    return jsonify(plate = car_data['plate'],
                   car = car_data['car'],
                   year = car_data['year'],
                   tax = car_data['tax'],
                   mot = car_data['mot'])

@app.route('/')
def extract_numberplate():

    secret_key = ''
    img_path = IMAGE_PATH

    with open(KEY_PATH) as txtfile:
        for line in txtfile:
            secret_key = line

    with open(img_path, 'rb') as image_file:
        img_base64 = base64.b64encode(image_file.read())

    url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=eu&secret_key=%s' % (secret_key)
    r = requests.post(url, data = img_base64)
    json_data = json.dumps(r.json(), indent=2)
    json_data = json.loads(json_data)

    try:
        plate = json_data['results'][0]['plate']
        confidence = json_data['results'][0]['confidence']

        if confidence >= 90:
            print("Number Plate: ", plate, "\t", "Confidence: ", confidence)
            return plate
        else:
            print("Plate found but confidence too low!")
            return "Plate not found!"
    except IndexError as index_error:
        print("Plate not found!")
        return "Plate not found!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')