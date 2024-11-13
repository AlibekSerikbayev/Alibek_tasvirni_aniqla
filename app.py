# streamlit run ./app.py
import streamlit as st
import requests
import matplotlib.patches as patches  
import matplotlib.pyplot as plt  
from PIL import Image  
import pandas as pd  # Pandas kutubxonasini import qilish
from random import randrange  # Tasodifiy raqamlar uchun

st.markdown("# :rainbow[Tasvirlarni aniqlash]")  

# Tasvirni aniqlash
def image_detect(image):  
    files = {'image': image}  
    headers = {'X-Api-Key': f"{st.secrets['API_TOKEN']}"}  
    try:  
        response = requests.post(st.secrets['API_URL'], headers=headers, files=files)  
        if response.status_code == 200:  
            st.info("Dastur ishladi! Hammasi joyida ")
            return response.json()  
        else:  
            return f"Xatolik: {response.status_code}, {response.text}"  
    except Exception as e:  
        return f"Xatolik: {e}"  

st.markdown("> :green[Rasmni ushbu qismga yuklang]")  
image_file = st.file_uploader("Aniqlanayotgan tasvirni yuklang", type=['jpg', 'png','webp','jfif']) 

if image_file:  
    # Rasmni ochamiz va o'lchamini tekshiramiz
    image = Image.open(image_file)
    if image.size[0] > 2000 or image.size[1] > 2000:  # O'lchamni tekshiramiz
        st.error("Rasm o'lchami 2000x2000 pikseldan kichik bo'lishi kerak.")
    else:
        with st.spinner('Tasvir aniqlanayabdi, iltimos ozgina vaqt kutib turing...'):  
            row1, row2 = st.columns(2)  
            row1.image(image_file, caption='Dastlabki tasvir')  

            detect_result = image_detect(image_file)  
            if isinstance(detect_result, str):  # Agar xatolik bo'lsa  
                row2.error(detect_result)  
            else:
                data = []
                # Natijalarni ko'rsatish  
                for i in range(len(detect_result)):  
                    data.append(
                        {
                            "labels": detect_result[i]['label'],
                            'confidence': float(detect_result[i]['confidence'])
                        }
                    )
                dataFrame = pd.DataFrame(data)
                row2.dataframe(data, use_container_width=True)

                fig, ax = plt.subplots()  
                ax.imshow(image)  
                ax.axis('off')  
                colors = ['#e14c2c', '#c87765', '#2aad95', '#2dd549', '#24a076', '#cae128', '#ee7b15', '#164bc4', '#6f25cc', '#9832be', '#f12f70', '#d82429', '#ead62d' ,'#60d41e', '#6aa549', '#16cb97']
                # Har bir aniqlangan belgi uchun chiziq va matnni qo'shamiz  
                for item in detect_result:  
                    label = item['label']  
                    x1 = int(item['bounding_box']['x1'])  
                    y1 = int(item['bounding_box']['y1'])  
                    x2 = int(item['bounding_box']['x2'])  
                    y2 = int(item['bounding_box']['y2'])  

                    rect_width = x2 - x1 
                    rect_height = y2 - y1
                    rect = patches.Rectangle((x1, y1), rect_width, rect_height, linewidth=1, edgecolor=colors[randrange(len(colors))], facecolor='none')  

                    ax.add_patch(rect)  
                    ax.text(x1, y1 - 10, f'{label.capitalize()} ({x1}, {y1})', color='red', fontsize=8)  

                # Faqat bitta natijaviy rasmni chiqaramiz  
                st.pyplot(fig, use_container_width=True)

