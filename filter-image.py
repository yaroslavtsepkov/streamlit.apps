import PIL
import streamlit as st
import numpy as np
from PIL import Image, ImageFilter

def getImage(fileupload):
    try:
        img = Image.open(fileupload)
    except:
        print("Что-то пошло не так...")
    return img

def clearImage(img: Image.Image)->Image.Image:
    filtered_img = img.filter(ImageFilter.MedianFilter(size=int(st.sidebar.slider("Выберете степень фильтрации", min_value=3, max_value=9, step=2))))
    return filtered_img

def main():
    fileupload = st.file_uploader("Upload your photo, support *.png, *.jpg, *.jpeg formats",)
    if fileupload is not None:
        img = getImage(fileupload)
        st.image(img, caption="Ваше изображение")
        filtered_img = clearImage(img)
        st.image(filtered_img, caption="Изображение после фильтрации")    

if __name__ == "__main__":
    main()