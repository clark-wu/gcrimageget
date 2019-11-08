#coding=utf-8
import argparse,json,logging,multiprocessing,docker,os

logging.basicConfig(level=logging.DEBUG)
_log = logging.getLogger(__name__)

SYNC_OLDER = 0
SYNC_NEW = 1


def handleSyncOneImage(username,password,org, dst):
    client = docker.from_env()
    client.login(username=username, password=password)
    dstV = dst.split(":")
    image = client.images.pull(org)
    image.tag(repository=dstV[0], tag=dstV[1])
    client.images.push(repository=dstV[0], tag=dstV[1])
    _log.info("finish push " + dst)


def syncimages(images, username, password,type=SYNC_OLDER):
    #pool = multiprocessing.Pool(processes=4)
    #res = []
    for i in images:
        try:
            if type == SYNC_OLDER:
                org_image = i[0]
                dst_image = i[1]
            elif type == SYNC_NEW:
                org_image = i
                dst_image = username+"/"+os.path.split(org_image)[1]
            else:
                raise Exception("sync type error.")
            handleSyncOneImage(username, password, org_image, dst_image)
        except Exception as e:
            print(str(e))
        # tmpr = pool.apply_async(handleSyncOneImage, args=(username, password,i[0],i[1]))
        # res.append(tmpr)
    #pool.close()
    #pool.join()



if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument("actor", type=str, help="actor type:[sync,]")
    parse.add_argument("-f", "--imagesfile", default="images.json", type=str,help="imagesfile name.")
    parse.add_argument("-u", "--username", default="", type=str, help="docker registry username.")
    parse.add_argument("-p", "--password", default="", type=str, help="docker registry password.")
    parse.add_argument("-t", "--synctype", default=SYNC_OLDER, type=int, help="sync type 0:older,1:new.")
    args = parse.parse_args()
    images = json.load(open(args.imagesfile))
    if args.actor == "sync":
        syncimages(images, args.username, args.password, args.synctype)



