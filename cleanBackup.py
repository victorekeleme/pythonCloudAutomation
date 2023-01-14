import boto3
import schedule
from operator import itemgetter
from datetime import datetime

ec2_client = boto3.client('ec2', region_name='us-east-2')


def cleanBackUp():
    volumes = ec2_client.describe_volumes(
        Filters=[
            {
                'Name': 'tag:Name',
                'Values': ['jenkins', ]
            }
        ]
    )

    for volume in volumes['Volumes']:
        volumeId = volume['VolumeId']
        snapshots = ec2_client.describe_snapshots(
            OwnerIds=['self'],
            Filters=[
                {
                'Name' : 'volume-id',
                'Values' : [volumeId]
                }
            ]

        )

        sortedSnapshot = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'))


        for snapshot in sortedSnapshot[2:]:
            snapshotId = snapshot['SnapshotId']
            print(snapshotId)
            response =ec2_client.delete_snapshot(
                SnapshotId=snapshotId
            )
            print(f"Snapshot with ID:{snapshotId} for VolumeID:{volumeId} has been deleted at: {datetime.now()}")


schedule.every(20).seconds.do(cleanBackUp)

while True:
    schedule.run_pending()
