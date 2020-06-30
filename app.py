#!/usr/bin/python

import boto3
from six.moves import configparser
import sys
import logging
import time

class parse_config:
    def __init__(self,filename):
        self.filename = filename


    def parse_all_servers(self):
        for y,x in enumerate(config.options('instances'),start=1):
            yield {str(x.encode("utf-8").strip("'")).upper(): [y,config.get('instances', x).encode("utf-8").strip("'")]}
    
    def parse_region(self):
        return config.get('region_name','region')

class ec2_action:
    def __init__(self,service,region):
        self.service = service
        self.region = region
        self.conn = boto3.resource(self.service,region_name=self.region)

    def list_instances(self,servers):
        try:
            logging.info(" =============== CURRENT STATE ================ ")
            for x in servers:
                for instance in self.conn.instances.all():
                    if instance.id in x.values()[0][1]:
                        print("%-20s %s " % (x.keys()[0], instance.state['Name']))

                        logging.info(" {} {}".format(x.keys()[0],instance.state['Name']))
            logging.info(" ================================================")
        except Exception as e:
            logging.error(e)



    def start_instances(self,servers):
        started_count = 0
        servers_details = []
        count = 0

        for x in servers:
            print x.values()[0][0],  ". " + x.keys()[0]
            servers_details.append(x)

        try:
            choice_instance = input(" Please enter your choice : - ")
            for x in servers_details:
                if x.values()[0][0] == choice_instance:
                    logging.info("Selected choice {} from start instances ".format(choice_instance))
                    count = count + 1
                    for instance in self.conn.instances.all():
                        if instance.id == x.values()[0][1] and choice_instance == x.values()[0][0] and instance.state['Name'] != 'running':
                            logging.info(instance.start())
                            started_count = started_count + 1
                            print "Starting {} Server and instance id is {} .. will take atleast 10 mins ".format(x.keys()[0], instance.id)
                            break
            if count == 0 and  started_count == 0:
                print "Wrong Choice ..!!!"
                logging.info("Wrong Choice ..!!".format(choice_instance))
            elif count == 1 and started_count == 0:
                print "Server is already in running state .. please check"
                logging.info("Server is already in running state .. please check")
        except Exception:
            print "Wrong Choice ..!!"
            logging.info("Wrong Choice ..!!")


    def stop_instances(self,servers):
        stopped_count = 0
        servers_details = []
        count = 0

        for x in servers:
            print x.values()[0][0], ". " + x.keys()[0]
            servers_details.append(x)

        try:
            choice_instance = input(" Please enter your choice : - ")
            for x in servers_details:
                if x.values()[0][0] == choice_instance:
                    logging.info("Selected choice {} from start instances ".format(choice_instance))
                    count = count + 1
                    for instance in self.conn.instances.all():
                        if instance.id == x.values()[0][1] and choice_instance == x.values()[0][0] and instance.state['Name'] == 'running':
                            logging.info(instance.stop())
                            stopped_count = stopped_count + 1
                            print "Stopping {} Server and instance id is {} .. will take atleast 10 mins ".format(x.keys()[0], instance.id)
                            break
            if count == 0 and stopped_count == 0:
                print "Wrong Choice ..!!!"
                logging.info("Wrong Choice ..!!".format(choice_instance))
            elif count == 1 and stopped_count == 0:
                print "Server is already in stopped state .. please check"
                logging.info("Server is already in stopped state .. please check")
        except Exception:
            print "Wrong Choice ..!!"
            logging.info("Wrong Choice ..!!".format(choice_instance))


    def health_checks(self,servers):
            count_health = 0
            logging.info(" ============ Health Checks Status ================ ")
            for x in servers:
                for instance in self.conn.meta.client.describe_instance_status()['InstanceStatuses']:
                    if x.values()[0][1] == instance['InstanceId']:
                        print( '%-20s %-20s %-20s %-20s' % (x.keys()[0], instance['InstanceState']['Name'],[k['Status'] for k in instance['SystemStatus']['Details']][0],[k['Status'] for k in instance['InstanceStatus']['Details']][0]))
                        count_health = count_health + 1
                        try:
                            logging.info("{} {} {} {}".format(x.keys()[0], instance['InstanceState']['Name'],[k['Status'] for k in instance['SystemStatus']['Details']][0],[k['Status'] for k in instance['InstanceStatus']['Details']][0]))
                        except AttributeError as e:
                           logging.info("Caught exception ... !!!")


            if count_health == 0:
                print "No health checks data found .."
                logging.info("No health checks data found ..")

            logging.info(" ================================================== ")



if __name__ == '__main__':
    logging.basicConfig(filename="logs",format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',level=logging.INFO,filemode='a')
    logging.info("Execution started ")
    try:
        config = configparser.ConfigParser()
        config.read("ec2-details")
        read_file_obj = parse_config("ec2-details")
        ec2_obj = ec2_action('ec2',read_file_obj.parse_region().strip("'"))
        if read_file_obj.parse_all_servers():
            logging.info("Config file parse successfull and connected to EC2")
        else:
            logging.info("Invaild config file")
    except Exception as e:
        logging.critical(e)
        sys.exit()



    while True:
        print " ======== MENU ========= "
        print " 1. List Servers Status  "
        print " 2. Stop Instance        "
        print " 3. Start Instance       "
        print " 4. Health Checks        "
        print " 5. Exit                 "
        print " ========================"
        try:
            choice = input("Please enter your choice : - ")
        except Exception:
            print "Wrong choice ..!!!"
            logging.error("Wrong choice ..!!! {}")
        else:
            if choice == 5:
                print "Good Bye ..!!"
                logging.info("Exiting from main program..!!")
                sys.exit(0)
            elif choice == 1:
                logging.info("selected choice {} ".format(choice))
                ec2_obj.list_instances(read_file_obj.parse_all_servers())
            elif choice == 2:
                logging.info("selected choice {} ".format(choice))
                ec2_obj.stop_instances(read_file_obj.parse_all_servers())
            elif choice == 3:
                logging.info("selected choice {} ".format(choice))
                ec2_obj.start_instances(read_file_obj.parse_all_servers())
            elif choice == 4:
                logging.info("Selected choice {} ".format(choice))
                ec2_obj.health_checks(read_file_obj.parse_all_servers())
            else:
                print "Wrong choice ..!!!!!!"
                logging.error("Wrong choice ..!!! {}".format(choice))







