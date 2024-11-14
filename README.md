The Project’s Core Objective
The primary goal was to identify which files and or packages had files that are not needed most of the time.
Ask the file system

Data Collection
The project started with gathering two sets of data:
1.	A comprehensive list of all files on the system, detailing their paths, creation, and access times.
2.	A corresponding list mapping files to the packages they belong to.
Data Processing: GPT Chose pandas
Utilizing Python’s pandas library, the data sets were merged based on file paths. This step was crucial in aligning each file with its package, correlating access times in the process.
Analysis: Identifying Least Accessed Packages
The merged data was then grouped by package names, and for each package, the oldest access time of its files was determined. This provided a clear picture of which packages were least interacted with, indicating potential areas for security review.
Reporting: Focused on Security Implications
The final report listed packages sorted by the oldest access time of their files. This prioritization assists security practitioners in identifying packages that might require updates, patches, or even removal to maintain system integrity.
Why This Matters for Security Practitioners
•	Attack Surface Optimization: Removing or updating rarely used packages can reduce the system’s attack surface.
•	Proactive Maintenance: Regular analysis of file access patterns enables a proactive approach to system security, allowing for timely interventions.
Other approaches evaluated
SELinux, auditd, eBPF and AppArmour:
All of these systems perform real-time reporting and would create performance impacts as well as requiring substantial engineering to be sure to detect “all file utilization”.
![image](https://github.com/vigilent/Security/assets/1031599/06ece6b1-f041-4dbc-92ef-8f9da6833e15)


# File Access and Modification Analysis

## Overview

This program uses `find` to examine a directory tree or filesystem: for the last time a file was accessed or changed. It
also determines whether either of these events has happened since the file was created. This analysis is designed for
Ubuntu versions 20 and later.
It stores the last modification time and whether the file was access more than threshold seconds after it was modified

    This Application WhatsUnused.sh is in alpha the installer is still in alpha test"

## Usage

To use this program, provide a path to the directory or filesystem you want to analyze.

		Usage: $0 [OPTIONS]"
		  OPTIONS:"
		    -t, --threshold SECONDS"
		                     Set the time threshold in SECONDS (default: 600)."
		    -d, --directories DIRS"
		                     Specify a colon-separated list of directories to search."
		                     (default: all mounted ext4 file systems)."
		    -u, --unused_window SECONDS"
		                     Set the time window in days during which a file must not"
		                     have been modified or read to be considered unused (default: 30)."
		    -m, --monitor"
		                     Run in monitor loops with sort -u & sleep minutes between loops."
								    no -m run once"
				    				      -m=n>0 (monitor for N+1 iteration)"
		    						      -m=0 infinte loop"
		    -s, --sleep"
		                     In monitor mode sleep N minutes between find runs."
		    -D, --debug"
		                     Enable debug mode to output additional information."
		                     Debug also shortens the sleep time to 6 seconds"
		    -h       Show this help message and exit."
		"

# Find Command Output Explanation

This script uses the `find` command to locate files in a specified directory tree that have not been accessed or
modified within a certain time frame.
Line 2 of the file is a version string that hasn't been tested with csv readers
./collector2.sh,0,0,v1, ../.. /tmp,-xdev -type f ( -mtime +30 -o -atime +30 ) -printf
%p,%T@,%A@\n../../aws_security_incident_response.docx,1677433493.066,1677433519.457,ish+-:26.392

Outputs are:
#Unused.csv:
Files that have neither been modified nor accessed in the
#Unused.err:
##All the errors find encountered which should be 0 for a privileges user

##Timestamp Management in ext4 for further investigation

       relatime
           Update inode access times relative to modify or change time.
           Access time is only updated if the previous access time was
           earlier than or equal to the current modify or change time.
           (Similar to noatime, but it doesn’t break mutt(1) or other
           applications that need to know if a file has been read since
           the last time it was modified.)

           Since Linux 2.6.30, the kernel defaults to the behavior
           provided by this option (unless noatime was specified), and
           the strictatime option is required to obtain traditional
           semantics. In addition, since Linux 2.6.30, the file’s last
           access time is always updated if it is more than 1 day old.

       norelatime
           Do not use the relatime feature. See also the strictatime
           mount option.

       strictatime
           Allows to explicitly request full atime updates. This makes
           it possible for the kernel to default to relatime or noatime
           but still allow userspace to override it. For more details
           about the default system mount options see /proc/mounts.

       nostrictatime
           Use the kernel’s default behavior for inode access time
           updates.

       lazytime
           Only update times (atime, mtime, ctime) on the in-memory
           version of the file inode.

           This mount option significantly reduces writes to the inode
           table for workloads that perform frequent random writes to
           preallocated files.

           The on-disk timestamps are updated only when:

           •   the inode needs to be updated for some change unrelated
               to file timestamps

           •   the application employs fsync(2), syncfs(2), or sync(2)

           •   an undeleted inode is evicted from memory

           •   more than 24 hours have passed since the inode was
               written to disk.

       nolazytime
           Do not use the lazytime feature.

       suid
           Honor set-user-ID and set-group-ID bits or file capabilities
           when executing programs from this filesystem.

       nosuid
           Do not honor set-user-ID and set-group-ID bits or file
           capabilities when executing programs from this filesystem. In
           addition, SELinux domain transitions require permission
           nosuid_transition, which in turn needs also policy capability
           nnp_nosuid_transition.
