#coding=utf-8
import argparse,json,docker,logging

_log = logging.getLogger(__name__)

def pullimages(images):
    client = docker.from_env()
    for i in images:
        tmpV = i["org"].split(":")
        dstV = i["dst"].split(":")
        image = client.images.pull(tmpV[0],tag=tmpV[1])
        image.tag(repository=dstV[0],tag=dstV[1])

def pushimages(images,username,password):
    client = docker.from_env()
    client.login(username=username,password=password)
    try:
        client.ping()
    except Exception as e:
        _log.error(str(e))
    for i in images:
        dstV = i["dst"].split(":")
        client.images.push(repository = dstV[0], tag = dstV[1])


if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument("actor",type=str,help="actor type:[pull,push,pull-x,push-x]")
    parse.add_argument("-f", "--imagesfile", default="images.json", type=str,help="imagesfile name.")
    parse.add_argument("-u", "--username", default="", type=str, help="docker registry username.")
    parse.add_argument("-p", "--password", default="", type=str, help="docker registry password.")
    args = parse.parse_args()
    images = json.load(open(args.imagesfile))
    if args.actor == "pull":
        pullimages(images)
    elif args.actor == "push":
        pushimages(images,args.username,args.password)


