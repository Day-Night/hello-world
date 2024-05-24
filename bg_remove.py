import streamlit as st
from PIL import Image
from io import BytesIO
from ultralytics import YOLO

model_yolo = YOLO("./weights.onnx")
st.set_page_config(layout="wide", page_title="Image Background Remover")

st.write("## 油漆桶识别报警")
st.write(
    ":dog: 上传图片并显示油桶检测结果。检测结果可以通过右侧的下载按钮进行下载 :grin:"
)
st.sidebar.write("## Upload and download :gear:")

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Download the fixed image
def convert_image():
    # boxes = img[0].boxes  # Boxes object for bounding box outputs
    # img[0].save(filename='result.jpg')  # save to disk
    # buf = BytesIO()
    byte_im = Image.open('./result.png')
    imgByteArr = BytesIO()
    byte_im.save(imgByteArr, format='PNG')
    image_bytes = imgByteArr.getvalue()
    return image_bytes


def fix_image(upload):
    image = Image.open(upload)
    col1.write("Original Image :camera:")
    col1.image(image)
    print("the type is: ",type(upload))
    print("upload :",upload)

    if isinstance(upload,str):
        fixed = model_yolo(upload,stream=False)
    else:
        fixed = model_yolo(image,stream=False)
    col2.write("Detected Image :wrench:")
    for res in fixed:
        res.save(filename='result.png')
    image_2 = Image.open('./result.png')
    col2.image(image_2)
    st.sidebar.markdown("\n")
    st.sidebar.download_button("Download fixed image", convert_image(), "result.png", "image/png")


col1, col2 = st.columns(2)
my_upload = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if my_upload is not None:
    if my_upload.size > MAX_FILE_SIZE:
        st.error("The uploaded file is too large. Please upload an image smaller than 5MB.")
    else:
        fix_image(upload=my_upload)
else:
    fix_image("./oil.jpeg")
