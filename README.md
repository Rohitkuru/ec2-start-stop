# boto3-automation


Title

Ec2-start-stop

Description

Following program helps you to start/stop AWS ec2 machine from any command line.(e.g. windows/linux) .

Program provide menu which helps user to easily manage start/stop operation. Multiple machines can be start/stop simultaneously . Program parse instance id , region name and access and security keys from config file and connects to appropriate AWS account . Program works exactly same if you choose to use IAM role instead of AWS access/security keys


How to use:

Program comes with config file , which has following options to configure

instances -> Please provide "user friendly" name to instance and unique "instance-id" , separated by each line
region_name -> Please provide region name where ec2 machines are hosted (e.g. us-east-1) 
credentials -> Please provide Access key and security access keys or remove this section if you wish to use AWS ROLE for start / stop 

Logs : -

Program creates logs file in same location and keeps updating which helps us track machines start/stop timings. Also it helps to debug errors if any

Thanks
