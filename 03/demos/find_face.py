import json
import boto3

mySession = boto3.session.Session(profile_name="jf_admin", region_name="eu-west-2")
client = mySession.client("rekognition")
collectID = "hallPresidents"

find_rsp = client.search_faces_by_image(
    Image={
        "S3Object": {
            "Bucket": "aws-rek-immersionday-eu-west-2",
            "Name": "media/celebrity-recognition/benjamin-harrison-portrait.jpg",
        }
    },
    CollectionId=collectID,
    FaceMatchThreshold=85,
)

FaceMatches = find_rsp["FaceMatches"]

faceCount = len(FaceMatches)

print(f"matches = {faceCount}")
if faceCount > 0:
    for match in FaceMatches:
        face = match["Face"]
        # print(json.dumps(face, indent=2))
        print(f"Facial Match = {face['ExternalImageId']}")
