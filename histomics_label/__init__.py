import datetime
from girder import plugin
from girder import events
from girder.models.file import File
from girder.models.notification import Notification
import yaml


class GirderPlugin(plugin.GirderPlugin):
    DISPLAY_NAME = 'Histomics Label'
    CLIENT_SOURCE_PATH = 'web_client'

    def load(self, info):
        # add plugin loading logic here
        plugin.getPlugin('histomicsui').load(info)

        # Set up event handler for config file updates
        def onConfigUpdate(event):
            file = event.info["file"]
            if file.get("name") == ".histomicsui_config.yaml":
                with File().open(file) as f:
                    config = yaml.safe_load(f)
                initialTrainingParameters = {
                    'radius': config.get('radius', None),
                    'magnification': config.get('magnification', None),
                    'certainty': config.get('certainty', None),
                    'feature': config.get('feature', None)
                }
                Notification().createNotification(
                    type='histomics_label.config_updated',
                    data=initialTrainingParameters,
                    user=event.info["currentUser"],
                    expires=(datetime.datetime.now(datetime.timezone.utc) +
                                datetime.timedelta(seconds=30))
                    )

        events.bind('data.process', 'histomics_label', onConfigUpdate)
