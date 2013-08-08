import os
import subprocess
import time

# ===================
# = LSF Dispatching =
# ===================

def submit_to_LSF(queue, LSFopfile, duration, cmd_to_submit, mem_usage=None):
    # wrap command to submit in quotations
    cmd_to_submit = r"'%s'" % cmd_to_submit.strip(r'"')
    LSF_params = {'LSFoutput': LSFopfile,
                  'queue': queue,
                  'duration': duration}
    LSF_cmd = 'rbsub -q%(queue)s -W %(duration)s -o%(LSFoutput)s' % LSF_params
    if mem_usage != None:
        LSF_cmd += r' -R "rusage[mem=%d]"' % mem_usage
    cmd = ' '.join([LSF_cmd, cmd_to_submit])
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    #p.wait()
    return p.stdout.read().split('<')[1].split('>')[0]

def parse_LSF_report(filename):
    jobID = -1
    finished = False
    succeeded = False
    
    ip = open(filename)
    for line in ip:
        if line.startswith('Subject:') and 'Job' in line:
            jobID = line.split()[2].rstrip(':')
            if 'Done' in line or 'Exited' in line:
                finished = True
        if 'TERM_REQUEUE_ADMIN' in line:    # for when rbsub requeues
            finished = False
        if 'Successfully completed.' in line:
            succeeded = True
    ip.close()
    
    return (jobID,finished,succeeded)

def wait_for_LSF_jobs(jobIDs,logfiles,interval=120):
    while len(jobIDs) > 0:
        time.sleep(interval)        
        # parse logfiles to see which jobs finished in the interim
        for logfile in logfiles:
            if not os.path.exists(logfile): # (job not finished)
                continue
            (jobID,finished,succeeded) = parse_LSF_report(logfile)
            if jobID != -1 and finished and succeeded:
                jobIDs.remove(jobID)
                logfiles.remove(logfile)
            elif jobID != -1 and finished and not succeeded:
                raise ValueError, "Job %s failed" % jobID

# DEPRECATED: USES bjobs TO TEST FOR JOB COMPLETION
# def wait_for_LSF_jobs(PIDs,interval=30):
#     finished = False
#     while not finished:
#         time.sleep(interval)
#         p = subprocess.Popen('bjobs',shell=True,stdout=subprocess.PIPE)
#         #p.wait()
#         status = p.stdout.read().split('\n')
#         if status[0].split()[0] != 'JOBID':
#             finished = False
#             continue
#         runningprocesses = [line.split()[0] for line in status if line.split() != [] and line.split()[0] != 'JOBID']
#         finished = True
#         for pid in PIDs:
#             if pid in runningprocesses:
#                 finished = False