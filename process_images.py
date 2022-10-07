from PIL import Image
import os, sys, time
from datetime import date


# Verify 6 images were inputted
validQuantity = False
try:
    if len(sys.argv) == 7:
        validQuantity=True
except ValueError:
    print("Please submit 6 images at a time for processing")

# List of input images
# to test: python3 process_images.py img1.png img2.png img3.png img4.png img5.png img6.png
imgs = []
for i in sys.argv[1:]:
    imgs.append(i)

# Copy images into processed_images folder for long-term storage
# NOTE:duplicate email addresses will copy existing saved images
# NOTE: make sure directory is write enabled: sudo chmod -R a+rw prompt_builder
if os.path.exists("processed_images"):
    for i in imgs:
        os.system("cp " + i + " processed_images/")
else:
    os.mkdir("processed_images")
    for i in imgs:
        os.system("cp " + i + " processed_images/")

# Canvas = 8.5x11 inches at 300 DPI is 2250x3300px
# dalle2 images = 1024x1024px / 72 DPI
width = 2550
height = 3300

# Create blank canvas
canvas = Image.new("RGB", (width, height), color = (255, 255, 255))

# Slots are where the stickers are on the sheet. Slot coordinates are the upper left corner. They are in the list in the following order: 
# Top left, top right, middle left, middle right, bottom left, bottom right
slots = [(186,186),(1461,186),(186,1200),(1461,1200),(186,2211),(1461,2211)]

# Coordinates of where the Continual logo should be placed 
branding_pos = (0,0)

for i, item in enumerate(imgs):
    # Read each image
    img = Image.open(imgs[i])
    
    # Read continual logo
    branding = Image.open("Dalle_template.png")

    # Paste Continual logo onto dalle2 image
    img.paste(branding, branding_pos, mask=branding)

    # Resize dalle2 image to sticker size (3" at 300 DPI = 900x900px)
    img.thumbnail((900,900), Image.ANTIALIAS)
    
    # Paste Dalle2 image onto canvas
    canvas.paste(img, slots[i])

canvas.show()
canvas.save("ready_for_print.pdf", format="pdf")

# Send PDF to printer
#os.system('lp -d HP553 ready_for_print.pdf')

# Delete images from repo
for i in imgs:
    os.system('rm '+ i)

# Move PDF to long term storage. 
# Filename is the timestamp it was created at. 
os.system('mv ready_for_print.pdf processed_images/'+ str(date.today().strftime("%Y%m%d%H%M%S")) +"_"+ str(int(time.time())) + ".pdf")