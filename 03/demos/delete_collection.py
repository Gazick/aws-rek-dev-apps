import boto3

client = boto3.client("rekognition", "eu-west-2")

collectID = "hallPresidents"

response = client.delete_collection(CollectionId=collectID)

print(response["StatusCode"])
