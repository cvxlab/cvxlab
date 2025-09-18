from pathlib import Path
from PIL import Image


def crop_logo(
        path_in,
        path_out,
        padding=0
):
    img = Image.open(path_in)
    bbox = img.getbbox()  # (left, upper, right, lower)

    if bbox:
        left, upper, right, lower = bbox
        # Expand the box by `padding`, making sure not to go outside the image
        left = max(0, left - padding)
        upper = max(0, upper - padding)
        right = min(img.width, right + padding)
        lower = min(img.height, lower + padding)

        cropped = img.crop((left, upper, right, lower))
        cropped.save(path_out)
        return (left, upper, right, lower), cropped.size

    else:
        # if image is empty, just save as-is
        img.save(path_out)
        return None, img.size


if __name__ == "__main__":

    source_path = r"D:\git_repos\cvxlab\docs\source\_static"
    file_names = [
        "CVXlab_logo_color.png",
        "CVXlab_logo_bw.png",
    ]
    padding = 30

    for file_name in file_names:
        path_in = Path(source_path) / file_name
        path_out = Path(source_path) / f"{file_name.split('.')[0]}_cropped.png"
        bbox, size = crop_logo(path_in, path_out, padding=padding)
        print("Logo:", bbox, size)
