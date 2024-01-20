from django.shortcuts import render
from django.http import JsonResponse
# import cv2
# from barcode import decode
from pyzbar.pyzbar import decode
from .models import Scans, Products
from PIL import Image, ImageDraw  # Pillow library for image handling
from django.core.files.storage import default_storage
from pyzxing import BarCodeReader

# def barcode_reader(image):
#     img = cv2.imread(image)
      
#     # Decode the barcode image
#     detectedBarcodes = decode(img)
    
#     # If not detected then print the message
#     if not detectedBarcodes:
#         return dict(error="Barcode Not Detected or your barcode is blank/corrupted!")
#     else:
    
#         # Traverse through all the detected barcodes in image
#         for barcode in detectedBarcodes:  
        
#             # Locate the barcode position in image
#             (x, y, w, h) = barcode.rect
            
#             # Put the rectangle in image using 
#             # cv2 to highlight the barcode
#             cv2.rectangle(img, (x-10, y-10),
#                         (x + w+10, y + h+10), 
#                         (255, 0, 0), 2)
            
#             if barcode.data!="":
            
#             # Print the barcode data
#                 return dict(success="Barcode fetched", data={
#                     "product_id": barcode.data,
#                     "type": barcode.type
#                 })
#                 # print(barcode.data)
#                 # print(barcode.type)
                 
#     #Display the image
#     # cv2.imshow("Image", img)
#     # cv2.waitKey(0)
#     # cv2.destroyAllWindows()
    
def barcode_reader2(image_path):
    # Open the image using Pillow
    img = Image.open(image_path)
    
    # Decode the barcode image
    detected_barcodes = decode(img)
    
    # If not detected, print the message
    if not detected_barcodes:
        return {"error": "Barcode Not Detected or your barcode is blank/corrupted!"}
    else:
        # Traverse through all the detected barcodes in the image
        for barcode in detected_barcodes:  
            # Extract barcode data
            barcode_data = barcode.data.decode('utf-8')
            barcode_type = barcode.type
            
            # Extract barcode position
            (x, y, w, h) = barcode.rect
            
            # Highlight the barcode on the image
            img = img.convert("RGB")  # Ensure that the image is in RGB mode
            draw = ImageDraw.Draw(img)
            draw.rectangle([x-10, y-10, x+w+10, y+h+10], outline="red", width=2)
            
            # Print the barcode data
            return {
                "success": "Barcode fetched",
                "data": {
                    "product_id": barcode_data,
                    "type": barcode_type
                }
            }

# def barcode_reader3(image_path):
#     # Open the image using Pillow
#     img = Image.open(image_path)

#     # Convert image to grayscale (ZXing works better with grayscale images)
#     img = img.convert("L")

#     # Create a BarCodeReader instance
#     barcode_reader = BarCodeReader()

#     # Decode the barcode image
#     decoded_barcodes = barcode_reader.decode(img)

#     # If not detected, print the message
#     if not decoded_barcodes:
#         return {"error": "Barcode Not Detected or your barcode is blank/corrupted!"}
#     else:
#         # Extract data from the first detected barcode
#         barcode_data = decoded_barcodes[0].data
#         barcode_type = decoded_barcodes[0].format

#         # Print the barcode data
#         return {
#             "success": "Barcode fetched",
#             "data": {
#                 "product_id": barcode_data,
#                 "type": barcode_type
#             }
#         }

class ProductService:
    def scan_code(self, request, **kwargs):
        # Assuming the uploaded image is in the 'image' field of the form
        image = kwargs.get("image")
        scanned_img = Scans.objects.create(scan_image=image)
        scanned_img.save()
        # Get the file path from the storage system
        file_path = default_storage.path(scanned_img.scan_image.name)

        data = barcode_reader2(str(file_path))
        scanned_img.delete()
        return data
        # return dict(success="Image scanned",data={})
        # print(image)
        
    def fetch_products(self, request):
        # Fetch products
        products = Products.objects.all()
        data = self.serialize_products(products)
        return dict(success="Products fetched", data=data)
        
    def serialize_products(self, products):
        first = products[0]
        products_data = [
            {
                "product_id": product.product_id,
                "product_name": product.product_name,
                "product_image": product.product_image_url,
                "brand": product.brand,
                "description": product.description,
                "price": product.price,
                "size": product.size,
                "discount": product.discount,
                "active": product.active,
                "expiry_date": product.exp_date,
                "category": {
                    "name": product.category.category_name
                },
                "date_created": product.created
            } for product in products
        ]
        
        return products_data
        