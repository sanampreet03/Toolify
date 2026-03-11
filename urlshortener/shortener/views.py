from django.shortcuts import render, redirect
from urllib.parse import urlparse
import qrcode
from io import BytesIO
import base64
from django.http import HttpResponse
import zipfile
from PIL import Image

url_database = {}

def home(request):
    short_url = None
    qr_code = None
    error = None

    if request.method == "POST":
        url = request.POST.get("url")

        # validate URL
        if not url or not url.startswith("http"):
            error = "Please enter a valid URL"
        else:
            code = "abc123"  # example short code
            url_database[code] = url

            short_url = request.build_absolute_uri('/') + code

            # generate QR code
            qr = qrcode.make(short_url)
            buffer = BytesIO()
            qr.save(buffer, format="PNG")

            qr_code = base64.b64encode(buffer.getvalue()).decode()

    return render(request, "index.html", {
        "short_url": short_url,
        "qr_code": qr_code,
        "error": error
    })


def redirect_url(request, code):
    url = url_database.get(code)

    if url:
        parsed = urlparse(url)
        main_site = f"{parsed.scheme}://{parsed.netloc}"
        return redirect(main_site)

    return redirect('/')

def file_compress(request):
    if request.method == "POST":
        uploaded_file = request.FILES["file"]

        buffer = BytesIO()

        # create zip file
        with zipfile.ZipFile(buffer, "w") as zip_file:
            zip_file.writestr(uploaded_file.name, uploaded_file.read())

        response = HttpResponse(buffer.getvalue(), content_type="application/zip")
        response['Content-Disposition'] = 'attachment; filename="compressed.zip"'

        return response

    return render(request, "file_compress.html")


def image_compress(request):
    if request.method == "POST" and request.FILES.get("image"):
        uploaded_image = request.FILES["image"]

        image = Image.open(uploaded_image)

        # convert RGBA to RGB
        if image.mode == "RGBA":
            image = image.convert("RGB")

        buffer = BytesIO()

        image.save(buffer, format="JPEG", quality=40, optimize=True)

        response = HttpResponse(buffer.getvalue(), content_type="image/jpeg")
        response['Content-Disposition'] = 'attachment; filename="compressed.jpg"'

        return response

    return render(request, "image_compress.html")