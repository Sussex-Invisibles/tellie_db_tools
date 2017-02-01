import couchdb
import argparse
import sys


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p",type=str,dest='password',help="CouchDB password")
    parser.add_argument("-f",type=str,dest='fibre',default=None,help="Fibre to find corresponding channel")
    parser.add_argument("-c",type=str,dest='channel',default=None,help="Channel to find corresponding Fibre")
    args = parser.parse_args()
    if(args.channel is not None and args.fibre is not None):
        print "Add either fibre or channel to get correspoding channel or fibre not both"
        sys.exit(1)
    highestRun = 0
    highestID = 0
    server = couchdb.Server("http://snoplus:"+args.password+"@couch.snopl.us")
    tellieDB = server["telliedb"]
    for row in tellieDB.view('_design/mapping/_view/map_by_run'):
          runNum = int(row.key[0])
          if runNum > highestRun:
              highestRun = runNum
              highestID = row['id']
    runDoc = tellieDB.get(highestID)
    channels = runDoc['channels']
    fibres = runDoc['fibres']
    if args.channel is None:
        fibreChanDict = dict(zip(fibres,channels))
        print "Fibre: %s corresponding channel %s" % (args.fibre,fibreChanDict[args.fibre])
        sys.exit(0)
    if args.fibre is None:
        chanFibreDict = dict(zip(channels,fibres))
        print "Channel: %s corresponding fibre %s" % (args.channel,chanFibreDict[args.channel])
        sys.exit(0)

