"""Validación del contenido real y almacenamiento privado con nombres aleatorios."""
import warnings
from pathlib import Path
from uuid import uuid4

from django.core.files.storage import default_storage
from PIL import Image, UnidentifiedImageError
from pypdf import PdfReader
from pypdf.errors import PyPdfError
from rest_framework.exceptions import ValidationError

MAX_BYTES = 10 * 1024 * 1024
IMAGENES = {".png": ("PNG", "image/png"), ".jpg": ("JPEG", "image/jpeg"),
            ".jpeg": ("JPEG", "image/jpeg"), ".webp": ("WEBP", "image/webp")}


def guardar_archivo(archivo, *, carpeta, solo_imagen=False):
    extension = Path(archivo.name).suffix.lower()
    if archivo.size <= 0 or archivo.size > MAX_BYTES:
        raise ValidationError({"archivo": "El archivo debe pesar entre 1 byte y 10 MB."})
    tipo = None
    if extension in IMAGENES:
        formato, tipo = IMAGENES[extension]
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("error", Image.DecompressionBombWarning)
                with Image.open(archivo) as imagen:
                    if imagen.format != formato:
                        raise ValueError("Extensión diferente del contenido")
                    imagen.verify()
                archivo.seek(0)
                with Image.open(archivo) as imagen:
                    imagen.load()
        except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError,
                Image.DecompressionBombWarning):
            raise ValidationError({"archivo": "La imagen no es válida."}) from None
    elif not solo_imagen and extension == ".pdf":
        if archivo.read(5) != b"%PDF-":
            raise ValidationError({"archivo": "El documento no es un PDF válido."})
        archivo.seek(max(0, archivo.size - 1024))
        if b"%%EOF" not in archivo.read():
            raise ValidationError({"archivo": "El PDF está incompleto."})
        archivo.seek(0)
        try:
            documento = PdfReader(archivo, strict=True)
            if documento.is_encrypted or len(documento.pages) == 0:
                raise ValueError("Documento cifrado o sin páginas")
        except (PyPdfError, ValueError, OSError, KeyError):
            raise ValidationError({"archivo": "El PDF debe ser legible, sin cifrado y contener páginas."}) from None
        tipo = "application/pdf"
    elif not solo_imagen and extension == ".mp4":
        encabezado = archivo.read(16)
        if encabezado[4:8] != b"ftyp":
            raise ValidationError({"archivo": "El video no es un MP4 válido."})
        tipo = "video/mp4"
    else:
        raise ValidationError({"archivo": "Usa PNG, JPG o WebP." if solo_imagen else "Usa PDF, PNG, JPG, WebP o MP4."})
    if archivo.content_type != tipo:
        raise ValidationError({"archivo": "El tipo MIME no corresponde a la extensión y al contenido."})
    archivo.seek(0)
    ruta = default_storage.save(f"{carpeta}/{uuid4().hex}{extension}", archivo)
    return ruta, tipo, archivo.size


def borrar_archivo(ruta):
    if ruta:
        default_storage.delete(ruta)
