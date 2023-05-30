import json
import time

import boto3

client = boto3.client("rekognition")

start_response = client.start_label_detection(
    Video={"S3Object": {"Bucket": "rekog-video", "Name": "summer.mp4"}},
    NotificationChannel={
        "SNSTopicArn": "arn:aws:sns:eu-west-2:709308243990:rekogTopic",
        "RoleArn": "arn:aws:iam::709308243990:role/rekogRole",
    },
)

JobId = start_response["JobId"]

print(f"JobId = {str(JobId)}")

time.sleep(1)

sqs = boto3.client("sqs")

for counter in range(1, 60):  # Receive message from SQS queue
    sqs_response = sqs.receive_message(
        QueueUrl="https://sqs.eu-west-2.amazonaws.com/709308243990/rekogQueue",
        AttributeNames=["SentTimestamp"],
        MaxNumberOfMessages=1,
        MessageAttributeNames=["All"],
        VisibilityTimeout=0,
        WaitTimeSeconds=0,
    )

    try:
        # for message in sqs_response['Messages']:
        message = sqs_response["Messages"][0]
        receipt_handle = message["ReceiptHandle"]

        databody = json.loads(message["Body"])
        datamsg = json.loads(databody["Message"])
        msgstatus = datamsg["Status"]

        # Delete received message from queue
        sqs.delete_message(
            QueueUrl="https://sqs.eu-west-2.amazonaws.com/709308243990/rekogQueue",
            ReceiptHandle=receipt_handle,
        )
        print("Received and deleted message:")
        print(f"Status = {msgstatus}")
        if msgstatus == "SUCCEEDED":
            break
    except ValueError:
        time.sleep(10)
        print(f"waiting for response {counter * 10/600} sec ")

print("fetch results")

lables_response = client.get_label_detection(JobId=JobId)

with open("labels.json", "w", encoding="utf-8") as outfile:
    json.dump(lables_response, outfile, indent=2)

print("Save to file complete")
