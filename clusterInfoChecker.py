import boto3


ec2_client = boto3.client('eks', region_name='us-east-2')

#list clusters
clusters = ec2_client.list_clusters()['clusters']

for cluster in clusters:
    response = ec2_client.describe_cluster(
        name=cluster
    )

    cluster_info = response['cluster']
    cluster_name = cluster_info['name']
    cluster_status = cluster_info['status']
    cluster_version = cluster_info['version']
    cluster_endpoint = cluster_info['endpoint']

    print(f"####################{str(cluster_name).upper()}#####################")
    print(f"Cluster Version: {cluster_version}")
    print(f"Cluster Status: {cluster_status}")
    print(f"Cluster Endpoint: {cluster_endpoint}")
    print("#####################################################################")






