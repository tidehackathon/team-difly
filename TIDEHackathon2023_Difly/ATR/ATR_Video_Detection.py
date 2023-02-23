######################################################

####Automatic Target Recognition(ATR) Video Player####

######################################################


from ultralytics import YOLO

model = YOLO("ATR/best.pt")

model.predict(
    source="ATR/VIDEO_INPUT", #INPUT DIRECTORY
    conf=0.29,
    save=True,
    save_txt=True
)
#OUTPUT WILL BE SAVED IN THE NEW DIRECTORY runs/detect/predict
