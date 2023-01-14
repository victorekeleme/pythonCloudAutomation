import boto3


ec2_client_ohio = boto3.client('ec2', region_name='us-east-2')
ec2_resource_ohio = boto3.resource('ec2', region_name='us-east-2')

reservations_ohio = ec2_client_ohio.describe_instances()['Reservations']

instanceIds_ohio = []


for reservation in reservations_ohio:
    print(reservation)
    instances = reservation['Instances']
    for ins in instances:
        instanceIds_ohio.append(ins['InstanceId'])


response = ec2_resource_ohio.create_tags(
    Resources=instanceIds_ohio,
    Tags=[
        {
            'Key':'environment',
            'Value':'dev'
        },
    ]
)

print(instanceIds_ohio)