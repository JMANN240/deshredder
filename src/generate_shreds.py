from random import uniform, shuffle
from PIL import Image, ImageDraw, ImageFont

scale = 200

number_of_shreds = 20

rotated_shred_margin_pixels = 10

background_color = (255, 0, 0)

font = ImageFont.truetype('/usr/share/fonts/TTF/OpenSans-Regular.ttf', int(0.25*scale))

def draw_wrapping(draw, text, margin=0.02):
    line = []
    (x, y) = (int(page_width*margin), int(page_width*margin))
    for word in text.split(" "):
        line.append(word)
        (_, _, right, bottom) = draw.textbbox((x, y), " ".join(line), font=font, anchor='la')
        if right > int(page_width*(1-margin)):
            draw.text((x, y), " ".join(line[:-1]), fill=(0, 0, 0), font=font, anchor='la')
            y = bottom
            line = [word]
    draw.text((x, y), " ".join(line), fill=(0, 0, 0), font=font, anchor='la')

page_width = int(8.5*scale)
page_height = int(11*scale)

page_image = Image.new('RGB', (page_width, page_height), (255, 255, 255))

page_draw = ImageDraw.Draw(page_image)

draw_wrapping(page_draw, "This is a test of some text to see how well the wrapping works. Really it is a test to see if we can create a page digitally, having a high resolution, and then 'shred' it to make it seem like a real paper that was shredded. We need a high resolution to make sure that the samples are sufficient, with lower resolutions there could be some overlap between dark regions of the shreds. Basically, I just have to type a bunch here to fill up the page and make it look more impressive. I could do a 'Lorem Ipsum' kind of thing, but I don't really want to because I feel like that is a bit lame. About one third of the way down the page now. I am getting a bit hungry, so I will probably go get dinner after this. At Eastway, there are some things that sound good. I was looking at the menu and I saw grilled marinated chicken breast, which has a lot of protein and isn't fried. Last time, though, it was a bit raw. Lame. They also have some taco stuff at the gluten station. They say they have Mexican street corn, so I am going to take a look at that. My mom makes Mexican street corn, but I am not sure how authentic it is. Either way, I really like how it tastes. It's a little spicy and savory. My finacee makes this one kind of corn that is like honey cream corn and it is so good. I could just shovel 4 cans-worth of it into my mouth non-stop. Last time we made that was a few weekends ago when we made the burger sliders as well. Can you tell that I am getting hungrier? All I am talking about now is food. The page is almost full, so I don't have to go much longer. So yeah, hopefully midterms go well. I have three of them this week. Tuesday, thursday, and friday. It's ridiculous. Math professors love to give out two midterms. I am going to say that the page is sufficiently full now.")

page_image.save("generated_page.png")

shred_width = int(page_width / number_of_shreds)

shred_images = [page_image.crop((x * shred_width, 0, (x+1) * shred_width, page_height)) for x in range(0, number_of_shreds)]

rotated_shred_images = []
for shred_image in shred_images:
    theta = uniform(-30, 30)
    rotated_shred_image = shred_image.rotate(theta, expand=True, fillcolor=background_color)
    rotated_shred_images.append(rotated_shred_image)

total_rotated_shred_images_width = sum([rotated_shred_margin_pixels * 2 + rotated_shred_image.width for rotated_shred_image in rotated_shred_images])
max_rotated_shred_images_height = max([rotated_shred_margin_pixels * 2 + rotated_shred_image.height for rotated_shred_image in rotated_shred_images])

shuffle(rotated_shred_images)

shreds_image = Image.new('RGB', (total_rotated_shred_images_width, max_rotated_shred_images_height), background_color)

shred_x = rotated_shred_margin_pixels
shred_y = rotated_shred_margin_pixels
for rotated_shred_image in rotated_shred_images:
    shreds_image.paste(rotated_shred_image, (shred_x, shred_y))
    shred_x += rotated_shred_margin_pixels * 2 + rotated_shred_image.width

shreds_image.save("generated_shreds.png")