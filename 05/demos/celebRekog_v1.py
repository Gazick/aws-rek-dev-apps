from __future__ import print_function
import boto3
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

print("Loading function")

session = boto3.Session(region_name="eu-west-2")
s3_client = session.client("s3")


def draw_box(myimage, draw, boundingBox, width, linecolor, name):
    boxLeft = float(boundingBox["Left"])
    boxTop = float(boundingBox["Top"])
    boxWidth = float(boundingBox["Width"])
    boxHeight = float(boundingBox["Height"])
    imageWidth = myimage.size[0]
    imageHeight = myimage.size[1]
    rectX1 = imageWidth * boxLeft
    rectX2 = imageHeight * boxTop
    rectY1 = rectX1 + (imageWidth * boxWidth)
    rectY2 = rectX2 + (imageHeight * boxHeight)
    fontSans = ImageFont.truetype("FreeSans.ttf", 30)
    draw.text((rectX1 + width, rectX2 + width), name, fill=(255, 255, 0), font=fontSans)
    for i in range(width):
        draw.rectangle(
            ((rectX1 + i, rectX2 + i), (rectY1 - i, rectY2 - i)),
            fill=None,
            outline=linecolor,
        )


def run_rekognition(bucket, filename, download_path, upload_path):
    rekog_client = session.client("rekognition")
    cele_rsp = rekog_client.recognize_celebrities(
        Image={"S3Object": {"Bucket": bucket, "Name": filename}}
    )
    celebrity_faces = {}
    unrecognized_faces = {}
    draw = {}
    celebrity_faces = cele_rsp["CelebrityFaces"]
    unrecognized_faces = cele_rsp["UnrecognizedFaces"]
    with Image.open(download_path) as myimage:
        draw = ImageDraw.Draw(myimage)
        for cele_face in celebrity_faces:
            name = cele_face["Name"]
            print(name)
            face = cele_face["Face"]
            bounding_box = face["BoundingBox"]
            # print(boundingBox)
            draw_box(myimage, draw, bounding_box, 4, "green", name)
        for unknown in unrecognized_faces:
            bounding_box = unknown["BoundingBox"]
            draw_box(myimage, draw, bounding_box, 4, "red", "unknown")

        myimage.save(upload_path)


def lambda_handler(event, context):
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]
        print(f"Bucket = {bucket}, Key = {key}")
        download_path = "/tmp/input.jpg"
        # print(download_path)
        s3_client.download_file(bucket, key, download_path)
        upload_path = "/tmp/output.jpg"
        # print(upload_path)
        run_rekognition(bucket, key, download_path, upload_path)
        s3_client.upload_file(upload_path, bucket, "output/celeBoxed.jpg")
        s3_client.put_object_acl(
            ACL="public-read", Bucket=bucket, Key="output/celeBoxed.jpg"
        )
