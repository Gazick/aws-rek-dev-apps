import boto3

mySession = boto3.session.Session(profile_name="jf_admin", region_name="eu-west-2")
client = mySession.client("rekognition")
collectID = "hallPresidents"


def add_facial_information(face_name, filename):
    index_rsp = client.index_faces(  # pylint: disable=unused-variable
        CollectionId=collectID,
        Image={
            "S3Object": {"Bucket": "aws-rek-immersionday-eu-west-2", "Name": filename}
        },
        ExternalImageId=face_name,
    )
    print(f"{face_name}   added")


create_rsp = client.create_collection(CollectionId=collectID)
retcode = create_rsp["StatusCode"]
print(f"Status Code = {str(retcode)}")
if retcode != 200:
    print("could not create collection")
    exit()

add_facial_information(
    "BenjaminHarrison", "media/celebrity-recognition/benjamin-harrison-portrait.jpg"
)
add_facial_information(
    "GroverCleveland", "media/celebrity-recognition/grover-cleveland-portrait.jpg"
)
add_facial_information(
    "TheodoreRoosevelt", "media/celebrity-recognition/theodore-roosevelt-portrait.jpg"
)
add_facial_information(
    "WilliamHowardTaft", "media/celebrity-recognition/william-howard-taft-portrait.jpg"
)
add_facial_information(
    "WilliamMcKinley", "media/celebrity-recognition/william-mckinley-portrait.jpg"
)
