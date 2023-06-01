import boto3
import PIL.Image
import PIL.ImageDraw

BUCKET = "aws-rek-immersionday-eu-west-2"
# FILE = "media/celebrity-recognition/oscar-selfie.jpg" # generates ValueError: x1 must be greater than or equal to x0
FILE = "media/celebrity-recognition/many-celebs-in-one.jpg"


def draw_box(draw, boundingBox, width, linecolor):
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
    for i in range(width):
        draw.rectangle(
            ((rectX1 + i, rectX2 + i), (rectY1 - i, rectY2 - i)),
            fill=None,
            outline=linecolor,
        )


mySession = boto3.session.Session(profile_name="jf_admin", region_name="eu-west-2")
rek_client = mySession.client("rekognition")
s3_resource = mySession.resource("s3")


s3_resource.Bucket(BUCKET).download_file(FILE, "input.jpg")

cele_rsp = rek_client.recognize_celebrities(
    Image={"S3Object": {"Bucket": BUCKET, "Name": FILE}}
)

celebrityFaces = {}
unrecognizedFaces = {}
draw_dct = {}

celebrityFaces = cele_rsp["CelebrityFaces"]
unrecognizedFaces = cele_rsp["UnrecognizedFaces"]

with PIL.Image.open("input.jpg") as myimage:
    draw_dct = PIL.ImageDraw.Draw(myimage)
    for celeFace in celebrityFaces:
        print(celeFace["Name"])
        Face = celeFace["Face"]
        bounding_box = Face["BoundingBox"]
        print(bounding_box)
        draw_box(draw_dct, bounding_box, 4, "red")
    for unknown in unrecognizedFaces:
        bounding_box = unknown["BoundingBox"]
        draw_box(draw_dct, bounding_box, 4, "black")
    myimage.save("modified.jpg")
