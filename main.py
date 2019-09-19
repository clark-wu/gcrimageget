#coding=utf-8
import argparse,json,logging,multiprocessing,docker

logging.basicConfig(level=logging.DEBUG)
_log = logging.getLogger(__name__)

def handleSyncOneImage(username,password,org, dst):
    client = docker.from_env()
    client.login(username=username, password=password)
    dstV = dst.split(":")
    image = client.images.pull(org)
    image.tag(repository=dstV[0], tag=dstV[1])
    client.images.push(repository=dstV[0], tag=dstV[1])
    _log.info("finish push " + dst)


def syncimages(images, username, password):
    #pool = multiprocessing.Pool(processes=4)
    #res = []
    for i in images:
        try:
            handleSyncOneImage(username, password,i[0],i[1])
        except Exception as e:
            pass
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
    args = parse.parse_args()
    images = json.load(open(args.imagesfile))
    if args.actor == "sync":
        syncimages(images,args.username,args.password)



