# import boto3
#
# ec2_client = boto3.client('ec2')
# ec2_resource = boto3.resource('ec2')
#
# dev_vpc = ec2_resource.create_vpc(
#     CidrBlock="10.0.0.0/16"
# )
# dev_vpc.create_subnet(
#     CidrBlock="10.0.1.0/24"
# )
# dev_vpc.create_subnet(
#     CidrBlock="10.0.2.0/24"
# )
# dev_vpc.create_tags(
#     Tags=[
#         {
#             'Key': 'Name',
#             'Value': 'dev-vpc'
#         }
#     ]
# )
#
#
# all_available_vpcs = ec2_client.describe_vpcs()
#
# vpcs = all_available_vpcs['Vpcs']
# print(vpcs)
#
# for vpc in vpcs:
#     print(vpc['VpcId'])
#     cidrBlockAssociationSet = vpc['CidrBlockAssociationSet']
#     for assoc_cidr in cidrBlockAssociationSet:
#         print(f"CidrBlock: {assoc_cidr['CidrBlock']}, CidrState: {assoc_cidr['CidrBlockState']}")