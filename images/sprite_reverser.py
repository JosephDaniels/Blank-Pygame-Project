from PIL import Image
im = Image.open("female_run_cycle_right.png")
new = Image.new("RGB", (2700,189))

x = 0
for i in range(18):
    copy = im.copy()
    x = i*150
    copy = copy.crop((x, 0, x+150, 189))
    new.paste(copy, (2700-x-150, 0))
    print (x, 2700-x-150)

new.save("female_run_cycle_right_revised.png")