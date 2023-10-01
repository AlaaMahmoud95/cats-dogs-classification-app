import streamlit as st
import pickle as pk
import numpy as np
import tensorflow as tf
import cv2 as cv

# Preprocessor and deeplearning model for feature extraction
preprocessor = tf.keras.applications.imagenet_utils.preprocess_input
vgg = tf.keras.applications.VGG16(include_top=False,weights='imagenet')
# Load Trained ML Model
clf = pk.load(open("vgg_clf.sav",'rb'))


st.title("""Cats-Dogs Classification
         - Using Feature Extraction.`VGG16`""")


IMGS = st.file_uploader(label="Image To Predict", type=["png","jpg"],
                       accept_multiple_files=True,)

# Upload and Store then import image Tensors
data=[]
if IMGS:
    for img in IMGS:
        with open(img.name,'wb') as im:
            im.write(img.read())
            data.append(cv.imread(im.name))


IMG_SZ = 244

pred=st.button("Classify")
if pred:
    # Resize Images
    n_data = np.array([cv.resize((x),(IMG_SZ,IMG_SZ)) for x in data],dtype='uint8')
    # Preprocess Images
    pre_img = preprocessor(n_data)
    # Extract Features and reshape for ML model
    features = vgg.predict(pre_img)
    sh = features.shape
    features = features.reshape(-1,sh[1]*sh[2]*sh[-1])
    # Classify Images
    cla = clf.predict(features)
    # 0,1 to Cat,Dog
    tr_cla = lambda x:"Dog" if x==1 else "Cat"
    # Fixing Colors for visualization
    vis = [cv.cvtColor(x,cv.COLOR_BGR2RGB) for x in n_data]
    # Display Images with class as caption
    st.image(vis,caption=list(map(tr_cla,list(cla))))
