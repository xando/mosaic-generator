import argparse
import functools
import requests
import os

from clint.textui import progress


class _flickr(type):

    config = {
        "api_key": "1f141e23bb332b71eaef1ffa5d97ca96",
        "format": "json",
        "nojsoncallback":"1",
        "per_page": "500"
    }

    def api_call(cls, name, *args, **kwargs):
        url = "http://api.flickr.com/services/rest/"

        cls.config['method'] = "flickr.%s" % name.replace("_",".")
        cls.config.update(kwargs)

        return requests.get(url, params=cls.config).json

    def __getattr__(cls, name):
        return functools.partial(cls.api_call, name)


class flickr(object):
    __metaclass__ = _flickr


def download(args):

    if not os.path.exists(args.directory):
        os.mkdir(args.directory)

    photo_list = []
    query = flickr.groups_pools_getPhotos(group_id=args.group_id)
    for page in range(1, query['photos']['pages']+1):
        photo_list.extend(
            flickr.groups_pools_getPhotos(
                group_id=args.group_id,
                page=page
            )['photos']['photo']
        )

    for photo in progress.bar(photo_list):
        name = "%(id)s_%(secret)s_m.jpg" % photo
        response = requests.get(
            "http://farm%(farm)s.staticflickr.com/%(server)s/%(id)s_%(secret)s_m.jpg" % photo
        )

        open(os.path.join(args.directory, name), "w").write(response.content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate some mosaic')
    parser.add_argument('group_id', type=str)
    parser.add_argument('directory', type=str)

    args = parser.parse_args()

    download(args)