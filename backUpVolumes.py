import boto3
import schedule
from datetime import datetime


ec2_client = boto3.client('ec2', region_name='us-east-2')

def create_snapshot():
    volumes = ec2_client.describe_volumes(
        Filters=[
            {
                'Name': 'tag:Name',
                'Values': ['jenkins',]
            }
        ]
    )
    for volume in volumes['Volumes']:
        new_snapshot = ec2_client.create_snapshot(
            VolumeId=volume['VolumeId']
        )
        print(f"Snapshot backup for {volume['VolumeId']} has been created at: {datetime.now()}")


schedule.every(20).seconds.do(create_snapshot)

while True:
    schedule.run_pending()

