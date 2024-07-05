from django.conf import settings
from django.core.management.base import BaseCommand

import helpers

STATICFILES_VENDOR_DIR = getattr(settings, "STATICFILES_VENDOR_DIR")

VENDOR_STATIC_FILES = {
    "flowbite.min.css": "https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.css",
    "flowbite.min.js": "https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.js",
    "flowbite.min.js.map": "https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.js.map",
    "htmx.min.js": "https://unpkg.com/htmx.org@2.0.0",
}


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write("Downloading vendor static files...")
        completed_urls = []
        for name, url in VENDOR_STATIC_FILES.items():
            out_path = STATICFILES_VENDOR_DIR / name
            download_sucess = helpers.download_to_local(url, out_path)
            if download_sucess:
                completed_urls.append(url)
            else:
                self.stdout.write(self.style.ERROR(f"Failed to download {url}"))
        if set(completed_urls) == set(VENDOR_STATIC_FILES.values()):
            self.stdout.write(
                self.style.SUCCESS("All vendor static files downloaded successfully")
            )
        else:
            self.stdout.write(
                self.style.ERROR("Some vendor static files failed to download")
            )
