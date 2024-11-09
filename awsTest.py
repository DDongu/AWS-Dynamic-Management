import boto3

ec2 = boto3.client("ec2")


def list_instances():
    # 인스턴스 목록을 확인하는 함수
    try:
        print("Listing instances....")
        response = ec2.describe_instances()
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                print(
                    "[id] {}, [AMI] {}, [type] {:<10}, [state] {:<10}, [monitoring state] {}".format(
                        instance["InstanceId"],
                        instance["ImageId"],
                        instance["InstanceType"],
                        instance["State"]["Name"],
                        instance["Monitoring"]["State"]
                        # instance["Tags"][0]["Value"],
                    )
                )
    except Exception as e:
        print(f"Error: {e}")
        pass


def list_available_zones():
    # 사용 가능한 클라우드 Zone 확인하는 함수
    try:
        print("Available zones ....")
        response = ec2.describe_availability_zones()
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


def list_available_regions():
    # 사용 가능한 클라우드 Region 확인하는 함수
    try:
        print("Available regions ....")
        response = ec2.describe_regions()
        for regions in response["Regions"]:
            print(
                "[region] {:<15}, [endpoint] {}".format(
                    regions["RegionName"], regions["Endpoint"]
                )
            )
    except Exception as e:
        print(f"Error: {e}")
        pass


def start_instance(instance_id):
    # 특정 인스턴스를 시작하는 함수
    try:
        print(f"Starting .... {instance_id}")
        response = ec2.start_instances(InstanceIds=[instance_id])
        print(f"Successfully started instance {instance_id}")
    except Exception as e:
        print(f"Error: {e}")


def stop_instance(instance_id):
    # 특정 인스턴스를 중지하는 함수
    try:
        response = ec2.stop_instances(InstanceIds=[instance_id])
        print(f"Successfully stop instance {instance_id}")
    except Exception as e:
        print(f"Error: {e}")


def create_instance(ami_id):
    # 특정 이미지의 인스턴스를 생성하는 함수
    try:
        response = ec2.run_instances(
            ImageId=ami_id, InstanceType="t2.micro", MaxCount=1, MinCount=1
        )
        instance_id = response["Instances"][0]["InstanceId"]
        print(f"Successfully started EC2 instance {instance_id} based on AMI {ami_id}")
    except Exception as e:
        print(f"Error: {e}")


def reboot_instace(instance_id):
    # 특정 인스턴스를 재시작하는 함수
    try:
        print(f"Rebooting .... {instance_id}")
        response = ec2.reboot_instances(InstanceIds=[instance_id])
        print(f"Successfully rebooted instance {instance_id}")
    except Exception as e:
        print(f"Error: {e}")


def list_images():
    # 생성 가능한 이미지 목록을 확인하는 함수
    try:
        print("Listing images....")
        response = ec2.describe_images(Owners=["self"])
        for image in response["Images"]:
            print(
                "[ImageID] {}, [Name] {}, [Owner] {}\n".format(
                    image["ImageId"], image["Name"], image["OwnerId"]
                )
            )
    except Exception as e:
        print(f"Error: {e}")
        pass


def menu():
    while True:
        print("                                                            ")
        print("                                                            ")
        print("------------------------------------------------------------")
        print("           Amazon AWS Control Panel using SDK               ")
        print("------------------------------------------------------------")
        print("  1. list instance                2. available zones        ")
        print("  3. start instance               4. available regions      ")
        print("  5. stop instance                6. create instance        ")
        print("  7. reboot instance              8. list images            ")
        print("                                 99. quit                   ")
        print("------------------------------------------------------------")

        number = input("Enter an integer: ")
        if number == "1":
            list_instances()
        elif number == "2":
            list_available_zones()
        elif number == "3":
            instance_id = input("Enter instance id: ")
            if instance_id:
                start_instance(instance_id)
        elif number == "4":
            list_available_regions()
        elif number == "5":
            instance_id = input("Enter instance id: ")
            if instance_id:
                stop_instance(instance_id)
        elif number == "6":
            ami_id = input("Enter ami id: ")
            if ami_id:
                create_instance(ami_id)
        elif number == "7":
            instance_id = input("Enter instance id: ")
            if instance_id:
                reboot_instace(instance_id)
        elif number == "8":
            list_images()
        elif number == "99":
            print("bye!")
            break
        else:
            print("concentration!")


if __name__ == "__main__":
    menu()
