from renpybuild.context import Context
from renpybuild.task import task, annotator
import requests
import zipfile


@annotator
def annotate(c: Context):
    c.include("{{ install }}/cubism/Core/include")
    c.env("CUBISM", "{{ install }}/cubism")


@task(platforms="all")
def build(c: Context):
    c.clean()

    cubism_zip = "CubismSdkForNative-5-r.5.zip"
    cubism_dir = "CubismSdkForNative-5-r.5"
    cubism_url = (
        "https://cubism.live2d.com/sdk-native/bin/"
        "CubismSdkForNative-5-r.5.zip"
        "?event=cubism_sdk_download&sdk_type=Native&user_status=new"
        "&user_type=%E5%80%8B%E4%BA%BA&version=5-r.5&lang=en"
    )

    c.var("live2d", c.path("{{ root }}/live2d"))

    archive = c.path("{{ tmp }}/tars/" + cubism_zip)
    archive.parent.mkdir(parents=True, exist_ok=True)

    if not archive.exists():
        print("Downloading Live2D Cubism SDK 5-r.5.")
        temporary = archive.with_suffix(archive.suffix + ".tmp")
        with requests.get(cubism_url, stream=True, timeout=(30, 300)) as response:
            response.raise_for_status()
            with temporary.open("wb") as f:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)

        if not zipfile.is_zipfile(temporary):
            temporary.unlink(missing_ok=True)
            raise RuntimeError("Live2D Cubism SDK download is not a valid ZIP archive.")

        temporary.replace(archive)

    if not zipfile.is_zipfile(archive):
        raise RuntimeError("Cached Live2D Cubism SDK archive is not a valid ZIP archive.")

    c.run("unzip -q {{ tmp }}/tars/" + cubism_zip)

    c.rmtree("{{ install }}/cubism")
    c.run("mv " + cubism_dir + " {{ install }}/cubism")

    include = c.path("{{ install }}/cubism/Core/include/Live2DCubismCore.h")
    if not include.is_file():
        raise RuntimeError(f"Live2D SDK is missing {include.relative_to(c.root)}")
