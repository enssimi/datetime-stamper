import os
import piexif
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
from tkinter import filedialog

# define a function to add a date/time stamp to the selected photo
def add_timestamp():
    # get the path to the photo file
    photo_path = filedialog.askopenfilename(title="Select photo")

    # read the EXIF metadata from the photo
    try:
        exif_dict = piexif.load(photo_path)
    except piexif._exceptions.InvalidImageDataError:
        error_label.config(text="Error: Invalid image data.")
        return

    # extract the date and time information from the EXIF metadata
    if "Exif" in exif_dict and piexif.ExifIFD.DateTimeOriginal in exif_dict["Exif"]:
        date_time = exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal].decode("utf-8")
    else:
        error_label.config(text="Error: No date/time information found in photo metadata.")
        return

    # convert the date and time information to a datetime object
    date_time_obj = datetime.strptime(date_time, "%Y:%m:%d %H:%M:%S")

    # format the date and time information as a string
    date_time_str = date_time_obj.strftime("%Y-%m-%d %H:%M:%S")

    # specify the font and font size for the date/time stamp
    font = ImageFont.truetype("arial.ttf", 36)
    # specify the position for the date/time stamp (down left, down right, up left, or up right)
    position = position_var.get()

    # open the photo using the PIL library
    try:
        photo = Image.open(photo_path)
    except OSError:
        error_label.config(text="Error: Unable to open photo file.")
        return

    # create a drawing object for the photo
    draw = ImageDraw.Draw(photo)

    # get the width and height of the photo
    width, height = photo.size

    # get the width and height of the date/time stamp text
    text_width, text_height = draw.textsize(date_time_str, font)

    # specify the position for the date/time stamp based on the chosen corner
    if position == "down_right":
        x = width - text_width - 10
        y = height - text_height - 10
    elif position == "up_left":
        x = 10
        y = 10
    elif position == "up_right":
        x = width - text_width - 10
        y = 10
    else:
        x = 10
        y = height - text_height - 10

    # draw the date/time stamp on the photo
    draw.text((x, y), date_time_str, fill="white", font=font)

    # save the modified photo
    photo.save(photo_path)

    # update the success label
    success_label.config(text="Date/Time stamp added to photo successfully.")

# create a tkinter window
window = tk.Tk()
window.title("Add Date/Time Stamp to Photo")

# create a button to select the photo
select_button = tk.Button(window, text="Select Photo", command=add_timestamp)
select_button.pack(pady=10)

# create a label to display errors
error_label = tk.Label(window, fg="red")
error_label.pack()

# create a label to display success message
success_label = tk.Label(window, fg="green")
success_label.pack()

# create a radio button to select the position for the date/time stamp
position_var = tk.StringVar(value="down_right")

position_frame = tk.Frame(window)
position_frame.pack()

down_right_rb = tk.Radiobutton(position_frame, text="Bottom Right", variable=position_var, value="down_right")
down_right_rb.pack(side="left")

up_right_rb = tk.Radiobutton(position_frame, text="Top Right", variable=position_var, value="up_right")
up_right_rb.pack(side="left")

up_left_rb = tk.Radiobutton(position_frame, text="Top Left", variable=position_var, value="up_left")
up_left_rb.pack(side="left")

down_left_rb = tk.Radiobutton(position_frame, text="Bottom Left", variable=position_var, value="down_left")
down_left_rb.pack(side="left")

window.mainloop()