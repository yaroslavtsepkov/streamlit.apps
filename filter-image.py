import numpy as np 
from PIL import Image, ImageOps
import math
import matplotlib.pyplot as plt
import os
import streamlit as st
from skimage.morphology import erosion, dilation, opening, closing
from skimage.morphology import skeletonize
from skimage.morphology import square
from skimage.util import invert

def getImage(fileupload):
    try:
        temp = Image.open(fileupload)
        temp = np.array(ImageOps.grayscale(temp))
        return temp
    except:
        st.error("Что-то пошло не так")

def genNoisy(img, lvl):
    noise = np.ones_like(img) * lvl * (img.max() - img.min())
    noise[np.random.random(size=noise.shape) > 0.5] *= -1
    return noise
    
def getHistFigure(img:np.ndarray):
    histogram, axs = plt.subplots()
    axs = plt.hist(img.ravel(), bins=255,color="gray")
    # axs.xlabel("Значение серого")
    # axs.ylabel("Количество пикселей")
    return histogram


# def threshold_processing(img: np.ndarray, threshold: np.uint8)->np.ndarray:
#     output = np.where(img > threshold, 255, 0)
#     return output

def main():
    fileupload = st.file_uploader("Загрузите фотографию",)
    if fileupload is not None:
        img = getImage(fileupload)
        cols1, cols2 = st.beta_columns(2)
        with cols1:
            st.image(img, caption="Ваше изображение")
            st.markdown("Гистограмма изображения")
            st.pyplot(getHistFigure(img))
        with cols2:
            lvl = st.sidebar.select_slider("Размер элемента",options=np.arange(1,10,1))
            selem = square(lvl)
            func = st.sidebar.selectbox("Функция",["Эрозия","Дилатация","Открытие","Закрытие"])
            if func in "Эрозия":
                output = erosion(img, selem)
            elif func in "Дилатация":
                output = dilation(img, selem)
            elif func in "Открытие":
                output = opening(img, selem)
            elif func in "Закрытие":
                output = closing(img, selem)

            st.image(output, caption="{}".format(func))
            st.markdown("Гистограмма изображения")
            st.pyplot(getHistFigure(output))
            pass   

if __name__ == "__main__":
    main()