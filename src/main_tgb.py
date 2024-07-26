from taipy.gui import Gui, notify, download
from rembg import remove
from PIL import Image
from io import BytesIO
import taipy.gui.builder as tgb


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

    with tgb.Page() as page:
        tgb.toggle(theme=True)

        with tgb.layout("265px 1fr", columns__mobile="30 70"):
            with tgb.part("sidebar"):
                tgb.text("### Removing Background from image", mode="md")
                tgb.file_selector("{path_upload}", extensions=".png,.jpg", label="Upload your image", on_action=upload_image, class_name="fullwidth")

                with tgb.expandable(title="More options", expanded=False):
                    tgb.text("**Foreground threshold**", mode="md")
                    tgb.slider("{advanced_properties.alpha_matting_foreground_threshold}", max=500, label="Foreground threshold")
                    tgb.text("**Background threshold**", mode="md")
                    tgb.slider("{advanced_properties.alpha_matting_background_threshold}", max=50, label="Background threshold")
                    tgb.text("**Erosion size**", mode="md")
                    tgb.slider("{advanced_properties.alpha_matting_erode_size}", max=50, label="Erosion size")

                    tgb.button("Run with options", on_action=fix_image, class_name="plain fullwidth", active="{original_image}")
                
                tgb.file_download("{None}", label="Download result", on_action=download_image, active="{fixed}")

            with tgb.part("container"):
                tgb.text("# Background Remover", mode="md")

                tgb.text("""
Give it a try by uploading an image to witness the seamless removal of the background. You can download images in full quality from the sidebar.
This code is open source and accessible on [GitHub](https://github.com/Avaiga/demo-remove-background).
                """, mode="md")

                with tgb.layout("1 1"):
                    with tgb.part("card text-center", render="{original_image}"):
                        tgb.text("### Original Image 📷", mode="md")
                        tgb.image("{original_image}")
                    with tgb.part("card text-center", render="{fixed_image}"):
                        tgb.text("### Fixed Image 🔧", mode="md")
                        tgb.image("{fixed_image}")

    Gui(page=page).run(margin="0px", title='Background Remover')
