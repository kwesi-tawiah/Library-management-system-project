from PIL import Image
image = Image.new(mode="RGB", size=(400, 400), color="blue")

image.save("my_image.jpg")

image.show()
