import boto3

"""
us_e = boto3.client("EC2", region_name="us-east-2") # Ohio
us_w = boto3.client("EC2", region_name="us-west-2") # Oregon
ca_cen = boto3.client("EC2", region_name="ca-central-1")    # Canada Central
eu_frnk = boto3.client("EC2", region_name="eu-central-1")   # Frankfurt
eu_stkh = boto3.client("EC2", region_name="eu-north-1") # Stockholm
as_mb = boto3.client("EC2", region_name="ap-south-1")   # Mumbai
as_jpn = boto3.client("EC2", region_name="ap-northeast-1")  # Tokyo
as_syd = boto3.client("EC2", region_name="ap-southeast-2")  # Sydney"""

regions = ["us-east-2", "us-west-2", "ca-central-1", "eu-central-1", "eu-north-1", "ap-south-1", "ap-northeast-1", "ap-southeast-1"]
instance_ids = ["i-074970e09ec9140c9", "i-0e574a4cc825fe3e5", "i-014abf8dbed385185", "i-0e2e57e830cf772e7", "i-0ccaa191c9bfb7b8d", "i-08e19ca4500893b25", "i-089c2863214864be8", "i-04e75dfda0bf9ef82"]
def start_all():
    for region in regions:
        instance_id = instance_ids[regions.index(region)]
        ec2 = boto3.client("ec2", region_name=region)
        response = ec2.start_instances(InstanceIds=[instance_id], DryRun=False)
        print(response)

def stop_all():
    for region in regions:
            instance_id = instance_ids[regions.index(region)]
            ec2 = boto3.client("ec2", region_name=region)
            response = ec2.stop_instances(InstanceIds=[instance_id], DryRun=False)
            print(response)
#start_all()
stop_all()