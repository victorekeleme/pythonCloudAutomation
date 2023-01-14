import boto3
import schedule

ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')

# reservations = ec2_client.describe_instances()
# for reservation in reservations['Reservations']:
#     instances = reservation['Instances']
#     for  instance in instances:
#         print(f"Instance {instance['InstanceId']} is {instance['State']['Name']} on AvailabilityZone: {instance['Placement']['AvailabilityZone']}")

def check_instance_status():
    statuses = ec2_client.describe_instance_status()
    for status in statuses['InstanceStatuses']:
        ins_status = status['InstanceStatus']['Status']
        sys_status = status['SystemStatus']['Status']
        state = status['InstanceState']['Name']
        print(f"Instance {status['InstanceId']} is {state} on AvailabilityZone: {status['AvailabilityZone']} with instance status: {str(ins_status).title()} and system status: {str(sys_status).title()}")


schedule.every(10).seconds.do(check_instance_status)

while True:
    schedule.run_pending()