import boto3

ec2 = boto3.client('ec2')


def list_instances():
    try:
        response = ec2.describe_instances()
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                print("Instance: " + instance['InstanceId'])
                for securityGroup in instance['SecurityGroups']:
                    print("SG ID: {}, Name: {}".format(
                        securityGroup['GroupId'], securityGroup['GroupName']))
    except Exception as e:
        print('get_instance_error', e)
        pass


def menu():
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


if __name__ == "__main__":
    # while True:
    #     menu()
    list_instances()
