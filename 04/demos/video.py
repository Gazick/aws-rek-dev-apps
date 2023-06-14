import json
import time
import boto3

mySession = boto3.session.Session(profile_name="default", region_name="eu-west-2")
rek_client = mySession.client("rekognition")

start_response = rek_client.start_label_detection(
    Video={
        "S3Object": {
            "Bucket": "aws-rek-immersionday-gazi",
            "Name": "media/object-detection/video_sample.mp4",
        }
    },
    NotificationChannel={
        "SNSTopicArn": "arn:aws:sns:eu-west-2:375990225440:rekogTopic",
        "RoleArn": "arn:aws:iam::375990225440:role/rekogRole",
    },
)

JobId = start_response["JobId"]
print(f"JobId = {str(JobId)}")

time.sleep(1)

sqs = mySession.client("sqs")

for counter in range(1, 60):  # Receive message from SQS queue
    sqs_response = sqs.receive_message(
        QueueUrl="https://sqs.eu-west-2.amazonaws.com/375990225440/recogQueue",  # notice typo recog instead of rekog !!
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
            QueueUrl="https://sqs.eu-west-2.amazonaws.com/375990225440/recogQueue",
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

lables_response = rek_client.get_label_detection(JobId=JobId)

with open("labels.json", "w", encoding="utf-8") as outfile:
    json.dump(lables_response, outfile, indent=2)

print("Save to file complete")
