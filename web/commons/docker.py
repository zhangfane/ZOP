import json

from docker import APIClient

from web import app


class DockerClient(object):
    def __init__(self, base_url):
        self.client = APIClient(base_url=base_url, version='auto', timeout=30)
        self.auth_config = {
            'username': app.config['DOCKER_REGISTRY_AUTH'].get('username'),
            'password': app.config['DOCKER_REGISTRY_AUTH'].get('password')
        }

    def __repr__(self):
        return '<DockerClient %r>' % self.client.base_url

    def __del__(self):
        self.client.close()

    @property
    def api_version(self):
        return self.client.api_version

    def docker_info(self):
        return self.client.info()

    def pull_image(self, image, tag, stream=False):
        if stream:
            return self.client.pull(image, tag, auth_config=self.auth_config, stream=True)
        rst = self.client.pull(image, tag, auth_config=self.auth_config)
        last_message = json.loads(rst.split('\r\n')[-2])
        if last_message.get('error'):
            # raise APIError(last_message['error'])
            pass

    def prune_images(self, filters=None):
        return self.client.prune_images(filters=filters)
