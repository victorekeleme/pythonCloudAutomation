from operator import itemgetter
import boto3

'''
<=========Flow of execution===========>
#Initialized client and resource variables
#create a function that takes the tag value to get the instance_id
#use the instance_id from function to get the volumes attached to the instance
#get the first volume attached to the instance
#get all snapshots created from the volume
#sort to get the latest snapshot
#create a new volume with the snapshot_id
#check new volume state == available then attach volume to desired instance
'''

#Initialized client and resource variables
ec2_client = boto3.client('ec2', region_name='us-east-2')
ec2_resource = boto3.resource('ec2', region_name='us-east-2')

#create a function that takes the tag value to get the instance_id
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

#use the instance_id from function to get the volumes attached to the instance
volumes = ec2_client.describe_volumes(
    Filters=[{
        'Name':'attachment.instance-id',
        'Values':[instanceId('Jenkins-Server')]
    }]
)

#get the first volume attached to the instance
instance_volume = volumes['Volumes'][0]

#get all snapshots created from the volume
snapshots = ec2_client.describe_snapshots(
    OwnerIds=['self',],
    Filters=[{
        'Name':'volume-id',
        'Values': [instance_volume['VolumeId']]
    }]
)

#sort to get the latest snapshot
latest_snapshot = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True)[0]

#create a new volume with the snapshot_id
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


#check new volume state == available then attach volume to desired instance

while True:
    vol = ec2_resource.Volume(new_volume['VolumeId'])

    if vol.state == 'available':
        #attach volume to desired instance
        ec2_resource.Instance(instanceId('Jenkins-Server')).attach_volume(
            VolumeId=new_volume['VolumeId'],
            Device='/dev/xvdb'
        )
        break


