import asyncio
import logging

from .client import client
from .client import connection
from .client import watcher
from .model import Model

log = logging.getLogger(__name__)


class Controller(object):
    async def connect_current(self):
        """Connect to the current Juju controller.

        """
        self.connection = (
            await connection.Connection.connect_current_controller())

    async def disconnect(self):
        """Shut down the watcher task and close websockets.

        """
        if self.connection and self.connection.is_open:
            log.debug('Closing controller connection')
            await self.connection.close()
            self.connection = None

    async def add_model(
            self, name, cloud, credential, owner=None,
            config=None, region=None):
        """Add a model to this controller.

        :param str name: Name of the model
        :param dict config: Model configuration
        :param str credential: e.g. '<cloud>:<credential>'
        :param str owner: Owner username

        """
        model_facade = client.ModelManagerFacade()
        model_facade.connect(self.connection)

        log.debug('Creating model %s', name)

        model_info = await model_facade.CreateModel(
            cloud,
            config,
            credential,
            name,
            owner or self.connection.info['user-info']['identity'],
            region,
        )

        model = Model()
        await model.connect(
            self.connection.endpoint,
            model_info.uuid,
            self.connection.username,
            self.connection.password,
            self.connection.cacert,
            self.connection.macaroons,
        )

        return model

    def add_user(self, username, display_name=None, acl=None, models=None):
        """Add a user to this controller.

        :param str username: Username
        :param str display_name: Display name
        :param str acl: Access control, e.g. 'read'
        :param list models: Models to which the user is granted access

        """
        pass

    def change_user_password(self, username, password):
        """Change the password for a user in this controller.

        :param str username: Username
        :param str password: New password

        """
        pass

    def destroy(self, destroy_all_models=False):
        """Destroy this controller.

        :param bool destroy_all_models: Destroy all hosted models in the
            controller.

        """
        pass

    def disable_user(self, username):
        """Disable a user.

        :param str username: Username

        """
        pass

    def enable_user(self):
        """Re-enable a previously disabled user.

        """
        pass

    def kill(self):
        """Forcibly terminate all machines and other associated resources for
        this controller.

        """
        pass

    def get_models(self, all_=False, username=None):
        """Return list of available models on this controller.

        :param bool all_: List all models, regardless of user accessibilty
            (admin use only)
        :param str username: User for which to list models (admin use only)

        """
        pass

    def get_payloads(self, *patterns):
        """Return list of known payloads.

        :param str \*patterns: Patterns to match against

        Each pattern will be checked against the following info in Juju::

            - unit name
            - machine id
            - payload type
            - payload class
            - payload id
            - payload tag
            - payload status

        """
        pass

    def get_users(self, all_=False):
        """Return list of users that can connect to this controller.

        :param bool all_: Include disabled users

        """
        pass

    def login(self):
        """Log in to this controller.

        """
        pass

    def logout(self, force=False):
        """Log out of this controller.

        :param bool force: Don't fail even if user not previously logged in
            with a password

        """
        pass

    def get_model(self, name):
        """Get a model by name.

        :param str name: Model name

        """
        pass

    def get_user(self, username):
        """Get a user by name.

        :param str username: Username

        """
        pass
