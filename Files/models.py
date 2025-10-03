import subprocess
from io import BytesIO
from django.db import models
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from cloudinary_storage.storage import MediaCloudinaryStorage


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class File(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    premium = models.BooleanField(default=False)
    file = models.FileField(upload_to='file/' ,storage=MediaCloudinaryStorage())  # Store SVG files
    image = models.ImageField(upload_to='images/', null=True, blank=True ,storage=MediaCloudinaryStorage())
    code = models.TextField(blank=True)         # Optional: store code directly
    created_at = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        self.full_clean()

        # SVG content পড়ে code field এ রাখুন
        if self.file and not self.code:
            self.file.seek(0)
            self.code = self.file.read().decode('utf-8')
            self.file.seek(0)  # reset pointer for Cloudinary

        # PNG preview generate using Inkscape
        if self.file and self.file.name.endswith(".svg"):
            try:
                import tempfile, subprocess
                from django.core.files.base import ContentFile

                # temporary files ব্যবহার
                with tempfile.NamedTemporaryFile(suffix=".svg") as temp_svg, \
                    tempfile.NamedTemporaryFile(suffix=".png") as temp_png:

                    self.file.seek(0)  # pointer start
                    temp_svg.write(self.file.read())
                    temp_svg.flush()

                    # Inkscape command
                    subprocess.run([
                        "inkscape",
                        temp_svg.name,
                        "--export-type=png",
                        "--export-filename", temp_png.name
                    ], check=True)

                    temp_png.seek(0)
                    self.image.save(f"{self.name}.png", ContentFile(temp_png.read()), save=False)

                # Cloudinary ফাইল আপলোডের আগে আবার pointer reset
                self.file.seek(0)

            except Exception as e:
                raise ValidationError(f"SVG preview generation failed: {e}")

        super().save(*args, **kwargs)


    def __str__(self):
        return self.name
