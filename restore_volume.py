from operator import itemgetter

import boto3


ec2_client = boto3.client('ec2', region_name='us-east-2')
ec2_resource = boto3.resource('ec2', region_name='us-east-2')

def instanceId(tagValue):
    reservations = ec2_client.describe_instances()['Reservations']
    instances = reservations
    for instance in instances:
        for ins in instance['Instances']:
            key = str(ins['Tags'][0]['Key'])
            value = str(ins['Tags'][0]['Value'])
            if tagValue == value:
                instance_id = ins['InstanceId']
    return instance_id


volumes = ec2_client.describe_volumes(
    Filters=[{
        'Name':'attachment.instance-id',
        'Values':[instanceId('Jenkins-Server')]
    }]
)

instance_volume = volumes['Volumes'][0]

snapshots = ec2_client.describe_snapshots(
    OwnerId=['self',],
    Filters=[{
        'Name':'volume-id',
        'Values': [instance_volume['VolumeId']]
    }]
)

latest_snapshot = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True)[0]

new_volume = ec2_client.create_volume(
    SnapshotId=latest_snapshot['SnapshotId'],
    AvailabilityZone="us-east-2c",
    TagSpecifications=[
        {
            'ResourceType': 'volume',
            'Tags': [
                {
                    'Key':'Name',
                    'Value': 'Jenkins-Server'
                }
            ]
        }
    ]
)


ec2_resource.Instance(instanceId('Jenkins-Server')).attach_volume(
    VolumeId=new_volume['VolumeId'],
    Device='/dev/xvdb'
)
# VolumeId


