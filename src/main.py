from taipy.gui import Gui, notify
from rembg import remove
from PIL import Image
from io import BytesIO


path_upload = ""
path_download = "fixed_img.png"
original_image = None
fixed_image = None
fixed = False


page = """<|toggle|theme|>

<page|layout|columns=300px 1fr|
<|sidebar|
### Removing **Background**{: .color-primary} from your image

<br/>
Upload and download
<|{path_upload}|file_selector|on_action=fix_image|extensions=.png,.jpg|label=Upload original image|>

<br/>
Download it here
<|{path_download}|file_download|label=Download fixed image|active={fixed}|>
|>

<|container|
# Image Background **Eliminator**{: .color-primary}

🐶 Give it a try by uploading an image to witness the seamless removal of the background. You can download images in full quality from the sidebar.
This code is open source and accessible on [GitHub](https://github.com/Avaiga/demo-remove-background).
<br/>


<images|layout|columns=1 1|
<col1|card text-center|part|render={fixed}|
### Original Image 📷 
<|{original_image}|image|>
|col1>

<col2|card text-center|part|render={fixed}|
### Fixed Image 🔧 
<|{fixed_image}|image|>
|col2>
|images>

|>
|page>
"""


def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im


def fix_image(state):
    notify(state, 'info', 'Uploading original image...')
    image = Image.open(state.path_upload)
    
    notify(state, 'info', 'Removing the background...')
    fixed_image = remove(image)
    fixed_image.save("fixed_img.png")

    notify(state, 'success', 'Background removed successfully!')
    state.original_image = convert_image(image)
    state.fixed_image = convert_image(fixed_image)
    state.fixed = True

if __name__ == "__main__":
    Gui(page=page).run(margin="0px", title='Background Remover')
