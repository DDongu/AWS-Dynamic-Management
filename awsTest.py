import boto3
from aws_manager import AwsManger

ec2 = boto3.client("ec2")
ssm = boto3.client("ssm")
cloudwatch = boto3.client("cloudwatch")
AwsManger = AwsManger(ec2, ssm, cloudwatch)


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
        print("  9. condor status               99. quit                   ")
        print("------------------------------------------------------------")

        number = input("Enter an integer: ")
        if number == "1":
            result = AwsManger.list_instances()
        elif number == "2":
            result = AwsManger.list_available_zones()
        elif number == "3":
            instance_id = input("Enter instance id: ")
            if instance_id:
                result = AwsManger.start_instance(instance_id)
        elif number == "4":
            result = AwsManger.list_available_regions()
        elif number == "5":
            instance_id = input("Enter instance id: ")
            if instance_id:
                result = AwsManger.stop_instance(instance_id)
        elif number == "6":
            ami_id = input("Enter ami id: ")
            if ami_id:
                result = AwsManger.create_instance(ami_id)
        elif number == "7":
            instance_id = input("Enter instance id: ")
            if instance_id:
                result = AwsManger.reboot_instance(instance_id)
        elif number == "8":
            result = AwsManger.list_images()
        elif number == "9":
            instance_id = input("Enter instance id: ")
            if instance_id:
                result = AwsManger.condor_status(instance_id)
        elif number == "10":
            instance_id = input("Enter instance id: ")
            if instance_id:
                result = AwsManger.get_metrics_statistics(instance_id)
        elif number == "99":
            print("bye!")
            break
        else:
            print("concentration!")
        print(result)


if __name__ == "__main__":
    menu()
