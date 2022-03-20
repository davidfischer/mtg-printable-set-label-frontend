import logging
import subprocess
import tempfile
import zipfile
from pathlib import Path

from django.http import FileResponse
from django.shortcuts import render

from .forms import LabelGeneratorForm


log = logging.getLogger(__name__)  # noqa


def homepage(request):
    message = None
    if request.method == "POST":
        form = LabelGeneratorForm(request.POST)
        if form.is_valid():
            sets = form.cleaned_data["sets"]
            paper_size = form.cleaned_data["paper_size"]

            with tempfile.TemporaryDirectory() as tempdir:
                subprocess.check_call(
                    [
                        "mtglabels",
                        "--paper-size",
                        paper_size,
                        "--output-dir",
                        tempdir,
                        *sets,
                    ]
                )
                zipfile_path = Path(tempdir) / "labels.zip"
                with zipfile.ZipFile(zipfile_path, "w") as myzip:
                    path = Path(tempdir)
                    for f in path.glob("*.svg"):
                        myzip.write(f, arcname=f.name)
                    for f in path.glob("*.pdf"):
                        myzip.write(f, arcname=f.name)

                return FileResponse(open(zipfile_path, "rb"), filename="labels.zip")
    else:
        form = LabelGeneratorForm()

    return render(request, "frontend/homepage.html", {"form": form, "message": message})
