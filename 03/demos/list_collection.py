import json

import boto3

client = boto3.client("rekognition", "eu-west-2")
collectID = "hallPresidents"

response = client.list_faces(CollectionId=collectID, MaxResults=100)

print(json.dumps(response, indent=2))
