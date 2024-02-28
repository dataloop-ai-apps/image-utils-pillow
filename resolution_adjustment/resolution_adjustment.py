from PIL import Image
import dtlpy as dl
import os
import shutil


class ServiceRunner(dl.BaseServiceRunner):
    def __init__(self):
        pass

    @staticmethod
    def change_resolution(item: dl.Item, context: dl.Context):
        node = context.node
        width = node.metadata['customNodeConfig']['width']
        height = node.metadata['customNodeConfig']['height']
        remote_path = node.metadata['customNodeConfig']['remote_path']
        local_path = os.path.join(os.getcwd(), f'res_adjustment_{item.id}')
        os.makedirs(local_path, exist_ok=True)
        image_path = item.download(local_path=local_path)
        image = Image.open(image_path)
        image = image.resize((width, height), 1)
        output_path = os.path.join(local_path, f'resized_{item.name}')
        image.save(output_path)
        adjusted_image = item.dataset.items.upload(local_path=output_path,
                                                   remote_path=remote_path,
                                                   item_metadata={'user': {
                                                       'original_item_id': item.id}
                                                   })
        shutil.rmtree(local_path)
        return adjusted_image
