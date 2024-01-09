import re
from collections import OrderedDict
from typing import Dict, List, Union

from django.utils.encoding import force_str

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from io import BytesIO
from PIL import Image
# from moviepy.editor import VideoFileClip
from datetime import datetime
# import cloudinary.uploader

import tempfile
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile


def convert_to_temporary_uploaded_file(
    in_memory_file: InMemoryUploadedFile,
) -> TemporaryUploadedFile:
    # Create a temporary directory to store the file
    temp_dir = tempfile.mkdtemp()

    # Construct the temporary file path
    temp_file_path = f"{temp_dir}/{in_memory_file.name}"

    # Write the content of the in-memory file to the temporary file
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(in_memory_file.read())

    # Create a TemporaryUploadedFile instance
    temporary_uploaded_file = TemporaryUploadedFile(
        name=in_memory_file.name,
        content_type=in_memory_file.content_type,
        size=in_memory_file.size,
        charset=in_memory_file.charset,
    )

    # Set the file attribute of the TemporaryUploadedFile
    temporary_uploaded_file.file = temp_file

    return temporary_uploaded_file


class CustomPagination(PageNumberPagination):
    page_size = 8

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "current_page": self.page.number,
                "data": data,
            }
        )

    def get_link_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ]
            )
        )


class ResponseManager:
    """Utility class that abstracts how we create a DRF response"""

    @staticmethod
    def handle_response(
        data: Dict = None, errors: Dict = None, status: int = 200, message: str = ""
    ) -> Response:
        if data is None:
            data = {}
        if errors is None:
            errors = {}
        if errors:
            return Response(
                {"message": errors, "data": data, "status": False}, status=status
            )
        return Response(
            {"data": data, "message": message, "status": True}, status=status
        )

    @staticmethod
    def handle_paginated_response(
        paginator_instance: PageNumberPagination = PageNumberPagination(), data=None
    ) -> Response:
        if data is None:
            data = {}
        return paginator_instance.get_paginated_response(data)

    @staticmethod
    def handle_dict_paginated_response(
        paginator_instance: PageNumberPagination = PageNumberPagination(), data=None
    ) -> Response:
        if data is None:
            data = {}
        return paginator_instance.get_link_paginated_response(data)

    @staticmethod
    def paginate_response(
        queryset, request, serializer_=None, page_size=10, paginator=CustomPagination
    ):
        paginator_instance = paginator()
        paginator_instance.page_size = page_size
        if not serializer_:
            return ResponseManager.handle_paginated_response(
                paginator_instance,
                paginator_instance.paginate_queryset(queryset, request),
            )
        return ResponseManager.handle_paginated_response(
            paginator_instance,
            serializer_(
                paginator_instance.paginate_queryset(queryset, request), many=True
            ).data,
        )

    @staticmethod
    def paginate_dict_response(
        result, request, page_size=10, paginator=CustomPagination
    ):
        paginator_instance = paginator()
        queryset = tuple(result.items())
        paginator_instance.page_size = page_size
        return ResponseManager.handle_dict_paginated_response(
            paginator_instance, paginator_instance.paginate_queryset(queryset, request)
        )

    @staticmethod
    def paginate_list_response(
        result, request, page_size=10, paginator=CustomPagination
    ):
        paginator_instance = paginator()
        queryset = result
        paginator_instance.page_size = page_size
        return ResponseManager.handle_dict_paginated_response(
            paginator_instance, paginator_instance.paginate_queryset(queryset, request)
        )


# def generate_thumbnail(image_or_video):
#     if isinstance(image_or_video, InMemoryUploadedFile) or isinstance(
#         image_or_video, TemporaryUploadedFile
#     ):
#         extension = image_or_video.name.split(".")[-1].lower()

#         if extension in ["jpg", "jpeg", "png"]:
#             # Generate thumbnail for images using Pillow
#             image = Image.open(image_or_video)
#             image.thumbnail((720, 1280))  # Adjust thumbnail size as needed
#             thumbnail_io = BytesIO()
#             image.save(thumbnail_io, format="JPEG")  # Save as JPEG or other format
#             thumbnail_io.seek(0)
#             thumbnail = InMemoryUploadedFile(
#                 thumbnail_io,
#                 field_name=None,  # Use None to indicate it's not a file field
#                 name="thumbnail.jpg",  # Set a filename for the thumbnail
#                 content_type="image/jpeg",  # Set the content type
#                 size=len(thumbnail_io.getvalue()),  # Set the size
#                 charset=None,
#             )
#             response = cloudinary.uploader.upload(
#                 thumbnail_io, folder="thumbnails", format="jpg"
#             )

#             return response["url"]

#         elif extension in ["mp4", "avi", "mov"]:
#             # Generate thumbnail for videos using moviepy
#             if isinstance(image_or_video, InMemoryUploadedFile):
#                 image_or_video = convert_to_temporary_uploaded_file(image_or_video)
#                 video = VideoFileClip(image_or_video.temporary_file_path())
#             else:
#                 video = VideoFileClip(image_or_video.temporary_file_path())
#             thumbnail = video.get_frame(0)  # Get the frame at 0 seconds (first frame)
#             thumbnail_image = Image.fromarray(thumbnail)
#             thumbnail_image.thumbnail((700, 700))  # Adjust thumbnail size as needed
#             thumbnail_io = BytesIO()
#             thumbnail_image.save(
#                 thumbnail_io, format="JPEG"
#             )  # Save as JPEG or other format
#             thumbnail_io.seek(0)
#             thumbnail = InMemoryUploadedFile(
#                 thumbnail_io,
#                 field_name=None,
#                 name="thumbnail.jpg",
#                 content_type="image/jpeg",
#                 size=len(thumbnail_io.getvalue()),
#                 charset=None,
#             )
#             response = cloudinary.uploader.upload(
#                 thumbnail, folder="thumbnails", format="jpg"
#             )

#             return response["url"]
