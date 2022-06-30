# L2chain

## Prepare dependencies 

### YCSB workload
To get the YCSB workloads files, please visit https://github.com/brianfrankcooper/YCSB
1. ``cd workloads/ycsb``
2. Download the latest release of YCSB.
3. (On Linux) run ``download_ycsb/bin/ycsb.sh run basic -P download_ycsb/workloads/workloada >> workloada.txt`` (where workloada can be replaced by other workloads)
Then you can get text files contatining fileds like:
> UPDATE usertable \<user\> [ field="\<value\>" ]
> 
> READ usertable \<user\> [ \<all fields\>]
