import streamlit as st 
from PIL import Image
from PIL import ImageDraw
import requests
import io

#設定ファイル
SUBSCRIPTION_KEY = '5fcf45f7077e40cd8bebdedc3df9701f'
assert SUBSCRIPTION_KEY
face_api_url = 'https://20220212ota.cognitiveservices.azure.com/face/v1.0/detect'


st.title('顔認識アプリ')

#画像アップロード
uploaded_file = st.file_uploader('Choose an image...', type = 'jpg' )

if uploaded_file is not None:
    img = Image.open(uploaded_file)

    with io.BytesIO() as output:
        img.save(output, format="jPEG")
        binary_img = output.getvalue() #バイナリ取得 

        headers = {
            'Content-Type':'application/octet-stream',
            'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY
        }

        params = {
            'returnFaceId': 'true',
            'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
        }

        res = requests.post(face_api_url, params=params,headers=headers, data=binary_img)
        results = res.json()

        #画像出力（顔の位置情報取得）
        for result in results:
            rect = result['faceRectangle']
            attribute = result['faceAttributes']
            text = attribute['gender'] + "," + str(attribute['age'])
            draw = ImageDraw.Draw(img)
            draw.rectangle([(rect['left'],rect['top']), (rect['left']+rect['width'] ,rect['top']+rect['height'])], fill=None, outline='red', width=5)
            draw.text((rect['left'], rect['top']), text, fill=(255, 255, 255))
        
        st.image(img, caption='Uploaded Image.', use_column_width=True)
