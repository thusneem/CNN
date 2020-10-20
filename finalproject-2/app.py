import os
from flask import Flask, request, jsonify, render_template
from keras.preprocessing import image
from bs4 import BeautifulSoup
from keras import backend as K
import keras
import requests
import re
app = Flask(__name__,template_folder='/Users/iqbalsandhu/Desktop/finalproject-2')
app.config['UPLOAD_FOLDER'] = 'uploads'



idx2label = {0: 'apple_pie',1: 'caesar_salad',2: 'cannoli',3: 'cheesecake', 4: 'chicken_wings', 5: 'cup_cakes', 6: 'donuts',7: 'french_fries',8: 'grilled_cheese_sandwich',9: 'guacamole', 10: 'hamburger',
11: 'hot_and_sour_soup',
12: 'hot_dog',
13: 'ice_cream',
14: 'lasagna',
15: 'oysters',
16: 'pizza',
17: 'spaghetti_carbonara',
18: 'steak',
19: 'sushi',
20: 'tacos',
21: 'waffles'}

def load_model():
    global model
    global graph
    model = keras.models.load_model('/Users/iqbalsandhu/Desktop/finalproject-2/food_trained.h5')
    graph = K.get_session().graph

load_model()


def prepare_image(img):
    # Convert the image to a numpy array
    img = image.img_to_array(img)
    # Scale from 0 to 255
    img /= 255

    # Flatten into a 1x28*28 array 
    image_resized = img.flatten().reshape(-1, 7*7*512)
    # Return the processed feature array
    return image_resized


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    data = {}
    if request.method == 'POST':
        print(request)

        if request.files.get('file'):
            # read the file
            file = request.files['file']

            # read the filename
            filename = file.filename

            # create a path to the uploads folder
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Save the file to the uploads folder
            file.save(filepath)

            # Load the saved image using Keras and resize it to the mnist
            # format of 28x28 pixels
            image_size = (224, 224)
            im = image.load_img(filepath, target_size=image_size)

            # Convert the 2D image to an array of pixel values
            image_array = prepare_image(im)
            print(image_array)
            # Get the tensorflow default graph and use it to make predictions
            global graph
            with graph.as_default():

                # Use the model to make a prediction
                predicted_digit = model.predict_classes(image_array)[0]
                for k,v in idx2label.items():
                    if k == predicted_digit:
                        data['prediction'] = v

                    # indicate that the request was a success
                        data["success"] = True

                        url_cal = 'https://ndb.nal.usda.gov/ndb/search/list?fgcd=&manu=&lfacet=&count=&max=25&sort=default&qlookup={}&offset=&format=Abridged&new=&measureby=&ds=SR&order=asc&qt=&qp=&qa=&qn=&q=&ing='.format(data['prediction'])
                        response1 = requests.get(url_cal)
                        soup = BeautifulSoup(response1.text, 'lxml')
                        row = soup.findAll('td')[2]
                        newurl = 'https://ndb.nal.usda.gov'+ row.find('a')['href']
                        newresponse = requests.get(newurl)
                        newsoup = BeautifulSoup(newresponse.text, 'lxml')
                        unit = newsoup.find('td', text = 'kcal')

                        unitstr = str(unit)

                        numkcal= str(unit.find_next_sibling("td"))

                        unit = re.sub("<.*?>", "", unitstr)
                        numkcal = re.sub("<.*?>", "", numkcal)
                        data['calories'] = numkcal
                        
    return render_template('index.html', data = data)
            
if __name__ == "__main__":
    app.run(debug=True)

