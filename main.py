#coding=utf-8
import argparse,json,docker,logging

_log = logging.getLogger(__name__)

def syncimages(images,username,password):
    client = docker.from_env()
    client.login(username=username, password=password)
    for i in images:
        tmpV = i["org"].split(":")
        dstV = i["dst"].split(":")
        image = client.images.pull(tmpV[0],tag=tmpV[1])
        image.tag(repository=dstV[0],tag=dstV[1])
        client.images.push(repository=dstV[0], tag=dstV[1])


if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument("actor",type=str,help="actor type:[sync,]")
    parse.add_argument("-f", "--imagesfile", default="images.json", type=str,help="imagesfile name.")
    parse.add_argument("-u", "--username", default="", type=str, help="docker registry username.")
    parse.add_argument("-p", "--password", default="", type=str, help="docker registry password.")
    args = parse.parse_args()
    images = json.load(open(args.imagesfile))
    if args.actor == "sync":
        syncimages(images,args.username,args.password)



