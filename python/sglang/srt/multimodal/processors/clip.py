from typing import List, Union

from sglang.srt.managers.schedule_batch import Modality, MultimodalDataItem
from sglang.srt.models.clip import CLIPModel
from sglang.srt.multimodal.processors.base_processor import BaseMultimodalProcessor
from sglang.srt.utils import load_image


class ClipImageProcessor(BaseMultimodalProcessor):
    models = [CLIPModel]

    def __init__(self, hf_config, server_args, _processor):
        super().__init__(hf_config, server_args, _processor)

    async def process_mm_data_async(
        self, image_data: List[Union[str, bytes]], input_text, *args, **kwargs
    ):
        if isinstance(input_text, list):
            assert len(input_text) and isinstance(input_text[0], int)
            input_text = self._processor.tokenizer.decode(input_text)

        images = [load_image(image)[0] for image in image_data]

        image_inputs = self.process_mm_data(input_text=input_text, images=images)
        image_inputs["data_hashes"] = [hash(str(image_data))]
        image_inputs["input_ids"] = image_inputs["input_ids"].tolist()[0]
        image_inputs["mm_items"] = [
            MultimodalDataItem(
                feature=image_inputs["pixel_values"], modality=Modality.IMAGE
            )
        ]

        return image_inputs
