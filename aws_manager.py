import time


class AwsManger:
    def __init__(self, ec2, ssm):
        self.ec2 = ec2
        self.ssm = ssm

    def list_instances(self):
        # 인스턴스 목록을 반환하는 함수
        try:
            instances = []
            response = self.ec2.describe_instances()
            for reservation in response["Reservations"]:
                for instance in reservation["Instances"]:
                    instance_info = {
                        "id": instance["InstanceId"],
                        "ami": instance["ImageId"],
                        "type": instance["InstanceType"],
                        "state": instance["State"]["Name"],
                        "monitoringState": instance["Monitoring"]["State"],
                        "name": (
                            instance["Tags"][0]["Value"]
                            if "Tags" in instance
                            else "None"
                        ),
                    }
                    instances.append(instance_info)
            return instances
        except Exception as e:
            return f"Error: {e}"

    def list_available_zones(self):
        try:
            zones = []
            response = self.ec2.describe_availability_zones()
            for zone in response["AvailabilityZones"]:
                zones.append(
                    {
                        "zone_id": zone["ZoneId"],
                        "region": zone["RegionName"],
                        "zone_name": zone["ZoneName"],
                    }
                )
            return zones
        except Exception as e:
            return f"Error: {e}"

    def list_available_regions(self):
        try:
            regions = []
            response = self.ec2.describe_regions()
            for region in response["Regions"]:
                regions.append(
                    {"region": region["RegionName"], "endpoint": region["Endpoint"]}
                )
            return regions
        except Exception as e:
            return f"Error: {e}"

    def start_instance(self, instance_id):
        try:
            self.ec2.start_instances(InstanceIds=[instance_id])
            return f"Successfully started instance {instance_id}"
        except Exception as e:
            return f"Error: {e}"

    def stop_instance(self, instance_id):
        try:
            self.ec2.stop_instances(InstanceIds=[instance_id])
            return f"Successfully stopped instance {instance_id}"
        except Exception as e:
            return f"Error: {e}"

    def create_instance(self, ami_id):
        try:
            response = self.ec2.run_instances(
                ImageId=ami_id,
                InstanceType="t2.micro",
                IamInstanceProfile={"Name": "ec2-ssm-role"},
                MaxCount=1,
                MinCount=1,
                SecurityGroups=["HTCondor"],
            )
            instance_id = response["Instances"][0]["InstanceId"]
            return (
                f"Successfully started EC2 instance {instance_id} based on AMI {ami_id}"
            )
        except Exception as e:
            return f"Error: {e}"

    def reboot_instance(self, instance_id):
        try:
            self.ec2.reboot_instances(InstanceIds=[instance_id])
            return f"Successfully rebooted instance {instance_id}"
        except Exception as e:
            return f"Error: {e}"

    def list_images(self):
        try:
            images = []
            response = self.ec2.describe_images(Owners=["self"])
            for image in response["Images"]:
                images.append(
                    {
                        "image_id": image["ImageId"],
                        "name": image["Name"],
                        "owner": image["OwnerId"],
                    }
                )
            return images
        except Exception as e:
            return f"Error: {e}"

    def condor_status(self, instance_id):
        try:
            response = self.ssm.send_command(
                InstanceIds=[instance_id],
                DocumentName="AWS-RunShellScript",
                Parameters={"commands": ["condor_status"]},
            )
            time.sleep(1)
            command_id = response["Command"]["CommandId"]
            output = self.ssm.get_command_invocation(
                CommandId=command_id,
                InstanceId=instance_id,
            )
            return output["StandardOutputContent"]
        except Exception as e:
            return f"Error: {e}"
