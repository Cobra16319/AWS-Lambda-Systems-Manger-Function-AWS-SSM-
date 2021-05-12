import time
import json
import boto3

def lambda_handler(event, context):

    # boto3 client
    client = boto3.client('ec2')
    ssm = boto3.client('ssm')
    
    # getting instance information
    describeInstance = client.describe_instances()

    InstanceId=['i-add-your-ec2-instance-id']


    # looping through instance ids
    for instanceid in InstanceId:
        # command to be executed on instance
        response = ssm.send_command(
                InstanceIds=[instanceid],
                DocumentName="AWS-RunShellScript",
                DocumentVersion='$DEFAULT',
                Parameters={"workingDirectory":["/home/ec2-user"],"executionTimeout":["3600"],"commands":["./some.sh"]} # replace command_to_be_executed with command
                )

        # fetching command id for the output
        command_id = response['Command']['CommandId']
        
        time.sleep(3) # We may need to raise the seconds for execution
        
        # fetching command output
        output = ssm.get_command_invocation(
              CommandId=command_id,
              InstanceId=instanceid
            )
        print(output)

    return {
        'statusCode': 200,
        'body': json.dumps('Thanks for being awsome!!!!')
    }

