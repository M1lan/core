#!/usr/bin/python

import subprocess
import time

while True:
  # For completeness this should also create the backend and the HTTP load balancer
  zones = subprocess.check_output("gcloud compute zones list --format='value(NAME)'", shell=True)
  zoneList = zones.strip().split('\n')
  for i, zone in enumerate(zoneList):
    backendname = "retriever"
    templatename = "retriever-2"
    instancegroupname = "retriever-group-" + zone
    print i, zone, instancegroupname
    # Create the instance group
    subprocess.call("gcloud compute instance-groups managed create {} -q --zone={} --size=0 --template={}".format(instancegroupname, zone, templatename), shell=True)
    # Add it to backend
    subprocess.call("gcloud compute backend-services add-backend {} -q --instance-group={} --instance-group-zone={}".format(backendname, instancegroupname, zone), shell=True)
    # Scale the instance group if it's the appropriate hour
    unixhour = time.time() // 3600
    bucket = unixhour % len(zoneList)
    size = 10 if i == bucket else 0
    print unixhour, bucket, size
    subprocess.call("gcloud compute instance-groups managed resize {} -q --zone={} --size={}".format(instancegroupname, zone, size), shell=True)
  # Wait 30 minutes and redo
  time.sleep(1800)