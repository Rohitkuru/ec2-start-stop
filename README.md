# boto3-automation


Title

Ec2-start-stop

Description

Following program helps you to start/stop AWS ec2 machine from any command line.(e.g. windows/linux) .

Program provide menu which helps user to easily manage start/stop operation. Multiple machines can be start/stop simultaneously . Program parse instance id , region name from config file  and connects to appropriate AWS account . Programworks exactly same if you choose to use IAM role instead of AWS access/security keys


How to use:

Program comes with config file(ec2-details)  , which has following options to configure (Sample availble)

instances -> Please provide "user friendly" name to instance and unique "instance-id" , separated by each line.
region_name -> Please provide region name where ec2 machines are hosted (e.g. us-east-1) 
IAM ROLE ACCESS -> NO more action require if access will be maintain by IAM ROLE.

Credetials -> Please configure AWS ACCCESS KEY AND AWS SECURITY ACCESS KEY as per normal procedure by AWS.


Sample ec2-details file and log file is attached

Logs : -

Program creates logs file in same location and keeps updating which helps us track machines start/stop timings. Also it helps to debug errors if any

Thanks
