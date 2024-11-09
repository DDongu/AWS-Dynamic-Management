import time


class AwsManger:
    def __init__(self, ec2, ssm):
        self.ec2 = ec2
        self.ssm = ssm

    def list_instances(self):
        # 인스턴스 목록을 확인하는 함수
        try:
            print("Listing instances....")
            response = self.ec2.describe_instances()
            for reservation in response["Reservations"]:
                for instance in reservation["Instances"]:
                    print(
                        "[id] {}, [AMI] {}, [type] {:<10}, [state] {:<10}, [monitoring state] {}".format(
                            instance["InstanceId"],
                            instance["ImageId"],
                            instance["InstanceType"],
                            instance["State"]["Name"],
                            instance["Monitoring"]["State"],
                        ),
                        end="",
                    )
                    print(
                        f", [Name] {instance["Tags"][0]["Value"]}"
                        if "Tags" in instance
                        else ", [Name] None"
                    )

        except Exception as e:
            print(f"Error: {e}")
            pass

    def list_available_zones(self):
        # 사용 가능한 클라우드 Zone 확인하는 함수
        try:
            print("Available zones ....")
            response = self.ec2.describe_availability_zones()
            for zones in response["AvailabilityZones"]:
                print(
                    "[id] {}, [region] {:<15}, [zone] {:<15}".format(
                        zones["ZoneId"], zones["RegionName"], zones["ZoneName"]
                    )
                )
            print(
                f"You have access to {len(response['AvailabilityZones'])} Availability Zones."
            )
        except Exception as e:
            print(f"Error: {e}")
            pass

    def list_available_regions(self):
        # 사용 가능한 클라우드 Region 확인하는 함수
        try:
            print("Available regions ....")
            response = self.ec2.describe_regions()
            for regions in response["Regions"]:
                print(
                    "[region] {:<15}, [endpoint] {}".format(
                        regions["RegionName"], regions["Endpoint"]
                    )
                )
        except Exception as e:
            print(f"Error: {e}")
            pass

    def start_instance(self, instance_id):
        # 특정 인스턴스를 시작하는 함수
        try:
            print(f"Starting .... {instance_id}")
            response = self.ec2.start_instances(InstanceIds=[instance_id])
            print(f"Successfully started instance {instance_id}")
        except Exception as e:
            print(f"Error: {e}")

    def stop_instance(self, instance_id):
        # 특정 인스턴스를 중지하는 함수
        try:
            response = self.ec2.stop_instances(InstanceIds=[instance_id])
            print(f"Successfully stop instance {instance_id}")
        except Exception as e:
            print(f"Error: {e}")

    def create_instance(self, ami_id):
        # 특정 이미지의 인스턴스를 생성하는 함수
        try:
            response = self.ec2.run_instances(
                ImageId=ami_id,
                InstanceType="t2.micro",
                IamInstanceProfile={"Name": "ec2-ssm-role"},
                MaxCount=1,
                MinCount=1,
                SecurityGroups=["HTCondor"]
            )
            instance_id = response["Instances"][0]["InstanceId"]
            print(
                f"Successfully started EC2 instance {instance_id} based on AMI {ami_id}"
            )
        except Exception as e:
            print(f"Error: {e}")

    def reboot_instace(self, instance_id):
        # 특정 인스턴스를 재시작하는 함수
        try:
            print(f"Rebooting .... {instance_id}")
            response = self.ec2.reboot_instances(InstanceIds=[instance_id])
            print(f"Successfully rebooted instance {instance_id}")
        except Exception as e:
            print(f"Error: {e}")

    def list_images(self):
        # 생성 가능한 이미지 목록을 확인하는 함수
        try:
            print("Listing images....")
            response = self.ec2.describe_images(Owners=["self"])
            for image in response["Images"]:
                print(
                    "[ImageID] {}, [Name] {}, [Owner] {}\n".format(
                        image["ImageId"], image["Name"], image["OwnerId"]
                    )
                )
        except Exception as e:
            print(f"Error: {e}")
            pass

    def condor_status(self, instance_id):
        # condor_status 명령어를 실행해주는 함수
        try:
            print("Getting condor status ....")
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
            print(f"{'='*47} CONDOR STATUS {'='*47}")
            print(output["StandardOutputContent"])
            print(f"{'='*109}")
        except Exception as e:
            print(f"Error: {e}")
            pass
