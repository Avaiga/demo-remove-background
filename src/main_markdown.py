from taipy.gui import Gui, notify, download
from rembg import remove
from PIL import Image
from io import BytesIO


def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im


def upload_image(state):
    state.image = Image.open(state.path_upload)
    state.original_image = convert_image(state.image)
    state.fixed = False
    fix_image(state)


def fix_image(state, id=None, action=None):
    state.fixed = False
    notify(state, 'info', 'Removing the background...')
    fixed_image = remove(state.image,
                         alpha_matting=True if action is not None else False, # Apply options when the button is clicked
                         alpha_matting_foreground_threshold=int(state.advanced_properties['alpha_matting_foreground_threshold']),
                         alpha_matting_background_threshold=int(state.advanced_properties['alpha_matting_background_threshold']),
                         alpha_matting_erode_size=int(state.advanced_properties['alpha_matting_erode_size']))

    state.fixed_image = convert_image(fixed_image)
    state.fixed = True
    notify(state, 'success', 'Background removed successfully!')


def download_image(state):
    download(state, content=state.fixed_image, name="fixed_img.png")


if __name__ == "__main__":
    path_upload = ""
    original_image = None
    image = None
    fixed_image = None
    fixed = False
    advanced_properties = {"alpha_matting_foreground_threshold":240,
                        "alpha_matting_background_threshold":10,
                        "alpha_matting_erode_size":10}

    page = """<|toggle|theme|>
<page|layout|columns=265px 1fr|
<|sidebar|
### Removing **Background**{: .color-primary} from image

<|{path_upload}|file_selector|extensions=.png,.jpg|label=Upload your image|on_action=upload_image|class_name=fullwidth|>

<|More options|expandable|not expanded|
**Foreground threshold**

<|{advanced_properties.alpha_matting_foreground_threshold}|slider|max=500|>

**Background threshold**

<|{advanced_properties.alpha_matting_background_threshold}|slider|max=50|>

**Erosion size**
<|{advanced_properties.alpha_matting_erode_size}|slider|max=50|>

<|Run with options|button|on_action=fix_image|class_name=plain fullwidth|active={original_image}|>
|>

---

<|{None}|file_download|label=Download result|on_action=download_image|active={fixed}|>
|>

<|container|
# Background **Remover**{: .color-primary}

Give it a try by uploading an image to witness the seamless removal of the background. You can download images in full quality from the sidebar.
This code is open source and accessible on [GitHub](https://github.com/Avaiga/demo-remove-background).

<images|layout|columns=1 1|
<col1|card text-center|part|render={original_image}|
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

    Gui(page=page).run(margin="0px", title='Background Remover')
