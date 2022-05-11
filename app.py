import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras.utils import img_to_array
from tensorflow.keras.preprocessing.image import smart_resize
from mtcnn.mtcnn import MTCNN
from matplotlib.patches import Rectangle
import glob
import cv2


from PIL import Image

#-------------------
import time
import streamlit as st

import os



output_path=''
input_path=''

def mask_detect(img):
  model = keras.models.load_model("mask_detector_vgg19.h5")

  img_ary = img_to_array(img)
  detector = MTCNN()
  faces = detector.detect_faces(img_ary)
  plt.figure(figsize=(15, 12))
  plt.imshow(img)
  ax = plt.gca()
  for face in faces:
    x1, y1, width, height = face['box']
    x2, y2 = x1+width, y1+height

    pred = model.predict(smart_resize(img_ary[y1:y2, x1:x2], (256, 256)).reshape(1, 256, 256, 3));
    # print("prediction")
    # print(pred)
    if pred[0][0] >= pred[0][1]:
      txt = 'Without Mask'
      color = 'red'
    else:
      txt = 'With Mask'
      color = 'lime'
    
    rect = Rectangle((x1, y1), width, height, fill=False, color=color, linewidth=2)
    ax.add_patch(rect)
    ax.text(x1, y1-2, txt, fontsize=14, fontweight='bold', color=color)
  
  plt.savefig('./output_images/out.png', dpi=300,bbox_inches='tight')  
  # plt.show()
  
  
def run():
    test_path = ""

    images = [cv2.imread(file) for file in glob.glob(test_path+"/*")]
    # print('There are {} test images'.format(len(images)))
    # print(test_path)
    # print(images)
    scaled_images =[]
    for img in images:
      dim = (256,256)
      if img.shape<(256, 256):
        img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        print('resized')
      img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
      scaled_images.append(img)

    for image in scaled_images:
      mask_detect(image)
def local_css(file_name):
    """ Method for reading styles.css and applying necessary changes to HTML"""
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        
def clean_input():
   if file_extension=="jpg":          
       os.remove(input_path+'in.jpg')
       print("input image deleted")
   else:   
       os.remove(input_path+'in.png')
       print("input image deleted")

def clean_output():
    os.remove(output_path+'out.png')
    print("output image deleted")


       
def main():
    global file_extension
    local_css("styles.css")
    st.markdown('<h1 align="center">😷 Face Mask Detection</h1>', unsafe_allow_html=True)
    activities = ["Image", "Webcam"]
    st.set_option('deprecation.showfileUploaderEncoding', False)
    st.sidebar.markdown("# Mask Detection on?")
    choice = st.sidebar.selectbox("Choose among the given options:", activities)
    
    if choice == 'Image':
        st.markdown('<h2 align="center">Detection on Image</h2>', unsafe_allow_html=True)
        st.markdown("### Upload your image here ⬇")
        image_file = st.file_uploader("", type=['jpg','png'])  # upload image
        if image_file is not None:
            file_name=image_file.name
            split=file_name.split('.')
            file_extension=split[-1]
            our_image = Image.open(image_file)  # making compatible to PIL
            if file_extension=="jpg":          
                im = our_image.save(input_path+'in.jpg')
            else:
                im = our_image.save(input_path+'in.png')
            saved_image = st.image(image_file, caption='', use_column_width=True)
            st.markdown('<h3 align="center">Image uploaded successfully!</h3>', unsafe_allow_html=True)
            
            if st.button('Process'):
                #animation
                with st.spinner('processing...'):
                    time.sleep(5)
                run()
                image_out = Image.open(output_path+'out.png')
                st.image(image_out, use_column_width=True)
                clean_input()
                clean_output()

            
            
    if choice == 'Webcam':
        st.markdown('<h2 align="center">Detection on Webcam</h2>', unsafe_allow_html=True)
        st.markdown('<h2 align="center">available soon !!</h2>', unsafe_allow_html=True)
 
main()    
