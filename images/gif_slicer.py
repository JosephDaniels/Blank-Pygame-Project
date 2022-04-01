from PIL import Image
from PIL import GifImagePlugin

source_filename = "attack_animation3.gif"

im = Image.open(source_filename)
print(im.is_animated)
print(im.n_frames)

width, height = im.size
print (width, height)
num_frames = im.n_frames
print (num_frames)
new = Image.new("RGB", (num_frames*width,height))

x = 0
for cur_frame in range(num_frames):
    im.seek(cur_frame)
    copy = im.copy()
    copy = copy.convert("RGB")
    x = cur_frame*width
    new.paste(copy, (0+x, 0))
    print(cur_frame)

new_name = source_filename.strip(".gif")+"_revised"+str(num_frames)+".png"
new.save(new_name)