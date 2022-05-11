






from PIL import Image


#-------------------
import time
import streamlit as st

import os
from detect_app import run


output_path='./output_images'
input_path='./input_images'
def local_css(file_name):
    """ Method for reading styles.css and applying necessary changes to HTML"""
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        
def clean_input():
   if file_extension=="jpg":          
       os.remove(input_path+'/in.jpg')
       print("input image deleted")
   else:   
       os.remove(input_path+'/in.png')
       print("input image deleted")

def clean_output():
    os.remove(output_path+'/out.png')
    print("output image deleted")


       
def main():
    global file_extension
    local_css("css/styles.css")
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
                im = our_image.save(input_path+'/in.jpg')
            else:
                im = our_image.save(input_path+'/in.png')
            saved_image = st.image(image_file, caption='', use_column_width=True)
            st.markdown('<h3 align="center">Image uploaded successfully!</h3>', unsafe_allow_html=True)
            
            if st.button('Process'):
                #animation
                with st.spinner('processing...'):
                    time.sleep(5)
                run()
                image_out = Image.open(output_path+'/out.png')
                st.image(image_out, use_column_width=True)
                clean_input()
                clean_output()

            
            
    if choice == 'Webcam':
        st.markdown('<h2 align="center">Detection on Webcam</h2>', unsafe_allow_html=True)
        st.markdown('<h2 align="center">available soon !!</h2>', unsafe_allow_html=True)
 
main()    
