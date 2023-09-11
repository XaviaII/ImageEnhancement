import cv2
import pandas as pd
import matplotlib.pyplot as plt

from tqdm import tqdm

import time
import subprocess

color_map = {
    0: (0, 0, 255),  # Team 0
    1: (0, 255, 0),  # Team 1
    2: (0, 0, 100),  # Goalie Team 0
    3: (0, 100, 0),  # Goalie Team 1
    4: (255, 0, 0),  # Referee
    5: (100, 0, 0)  # Assistant Referee
}

def display_cv2_img(img, figize=(10, 10)):
    img_ = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    fig, ax = plt.subplots(figsize=figize)
    ax.imshow(img_)
    ax.axis("off")
    plt.show()

def add_rectangles(img, frame, labels):
    max_frame = labels.query("frame <= @frame")["frame"].max()
    frame_labels = labels.query("frame == @max_frame")
    for i, d in frame_labels.iterrows():
        # print(frame_labels)
        pt1 = int(d["x_top_left"]), int(d["y_top_left"])
        pt2 = int(d["x_top_left"] + d["width"]), int(d["y_top_left"] + d["height"])
        color = color_map[d["type"]]
        img = cv2.rectangle(img, pt1, pt2, color, 3)
    return img


video = "achau-02_left"

# import the Video
cap = cv2.VideoCapture("00_Original_Videos/" + video + ".mp4")
labels = pd.read_csv("00_Original_Videos/" + video + ".csv")

# read out importen Video informations
framecount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

# Export labeld video
VIDEO_CODEC = "MP4V"
out = cv2.VideoWriter(
          "original_videos/" + video + "_labeled.mp4",
          cv2.VideoWriter_fourcc(*VIDEO_CODEC),
          fps,
          (width, height)
      )

for frame in tqdm(range(framecount), total=framecount):
    ret, img = cap.read()
    # display_cv2_img(img)
    if ret == False:
        break
    img = add_rectangles(img, frame, labels)
    out.write(img)
    # display_cv2_img(img)

out.release()
cap.release()

