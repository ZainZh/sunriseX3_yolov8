import time
import cv2
import numpy as np

try:
    import onnxruntime as onnxruntime
except ImportError:
    onnxruntim = None
from src.yolov5.utils import postprocess
from src.yolov8.utils import draw_detections
from src.tools.common import print_info, load_omega_config, bgr2nv12_opencv

try:
    from hobot_dnn import pyeasy_dnn as dnn
except ImportError:
    dnn = None


class YOLOv5:
    def __init__(self, input_shape: list = (1, 3, 640, 640)):
        self.config = load_omega_config("YOLOv5")
        self.class_names = self.config["class_names"]
        self.conf_threshold = self.config["conf_thres"]
        self.iou_threshold = self.config["iou_thres"]

        self.boxes, self.scores, self.class_ids = [], [], []
        self.img_height, self.img_width = 0, 0
        self.input_height, self.input_width = input_shape[2], input_shape[3]

    def detect_objects(self, image):
        if image.ndim == 3:
            # RGB image
            input_tensor = self.prepare_input(image)
        else:
            # NV12 image
            input_tensor = image
            self.input_width, self.input_height = self.input_width, self.input_height
        # Perform inference on the image
        outputs = self.inference(input_tensor)
        self.boxes, self.scores, self.class_ids = self.process_output(outputs)

        return self.boxes, self.scores, self.class_ids

    def prepare_input(self, image):
        raise NotImplementedError

    def inference(self, input_tensor):
        raise NotImplementedError

    def get_boxes_labels_scores(self, nms_bboxes):
        for i, bbox in enumerate(nms_bboxes):
            class_index = int(bbox[5])
            score = bbox[4]
            self.boxes.append(bbox[:4])
            self.scores.append(score)
            self.class_ids.append(class_index)
    def process_output(self, output):
        """
        Process the output from the model to get the bounding boxes, class IDs, and scores.
        The shape of bbox is xyxy.
        Args:
            output:

        Returns:

        """
        nms_bboxes = postprocess(
            output,
            model_hw_shape=(self.input_width, self.input_height),
            origin_img_shape=(self.img_width, self.img_height),
        )
        self.get_boxes_labels_scores(nms_bboxes)
        return self.boxes, self.scores, self.class_ids


    def draw_detections(self, image, draw_scores=True, mask_alpha=0.4):
        return draw_detections(
            image, self.boxes, self.scores, self.class_ids, mask_alpha
        )


class YOLOv5ONNX(YOLOv5):
    def __init__(self, model):
        self.session = onnxruntime.InferenceSession(
            model, providers=onnxruntime.get_available_providers()
        )

        # get input details
        model_inputs = self.session.get_inputs()
        self.input_names = [model_inputs[i].name for i in range(len(model_inputs))]
        self.input_shape = model_inputs[0].shape

        # get output details
        model_outputs = self.session.get_outputs()
        self.output_names = [model_outputs[i].name for i in range(len(model_outputs))]
        self.output_shape = model_outputs[0].shape

        super().__init__(input_shape=self.input_shape)

        self.print_model_info()

    def __call__(self, image):
        return self.detect_objects(image)

    def prepare_input(self, image):
        self.img_height, self.img_width = image.shape[:2]

        input_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Resize input image
        input_img = cv2.resize(input_img, (self.input_width, self.input_height))

        # Scale input pixel values to 0 to 1
        input_img = input_img / 255.0
        input_img = input_img.transpose(2, 0, 1)
        input_tensor = input_img[np.newaxis, :, :, :].astype(np.float32)

        return input_tensor

    def inference(self, input_tensor):
        start = time.perf_counter()
        outputs = self.session.run(
            self.output_names, {self.input_names[0]: input_tensor}
        )

        # print(f"Inference time: {(time.perf_counter() - start) * 1000:.2f} ms")
        return outputs

    def print_model_info(self):
        model_info = {
            "input_names": self.input_names,
            "input_shape": self.input_shape,
            "output_names": self.output_names,
            "output_shape": self.output_shape,
        }
        for key, value in model_info.items():
            print_info(f"{key}:", value)


class YOLOv5BIN(YOLOv5):
    def __init__(self, model):
        self.model = dnn.load(str(model))
        self.model_input_properties = self.model[0].inputs[0].properties
        self.model_output_properties = self.model[0].outputs[0].properties

        # get input details
        self.input_shape = self.model_input_properties.shape  # get output details
        self.output_shape = self.model_output_properties.shape

        print("model_input_properties:===============")
        self.print_model_info(self.model_input_properties)
        print("model_output_properties:===============")
        self.print_model_info(self.model_output_properties)

        super().__init__(input_shape=self.input_shape)

    def __call__(self, image):
        return self.detect_objects(image)

    def inference(self, input_tensor):
        """

        Args:
            input_tensor: NV12 image

        Returns:

        """
        start = time.perf_counter()
        outputs = self.model[0].forward(input_tensor)
        # print(f"Inference time: {(time.perf_counter() - start) * 1000:.2f} ms")
        return outputs

    def prepare_input(self, image):
        start = time.perf_counter()
        self.img_height, self.img_width = image.shape[:2]
        # Resize input image
        input_img = cv2.resize(image, (self.input_width, self.input_height))
        input_img = bgr2nv12_opencv(input_img)
        # print(f"Preprocess time: {(time.perf_counter() - start) * 1000:.2f} ms")
        return input_img

    @staticmethod
    def print_model_info(property_name):
        model_info = {
            "tensor type": property_name.tensor_type,
            "data type": property_name.dtype,
            "layout": property_name.layout,
            "shape": property_name.shape,
        }

        for key, value in model_info.items():
            print_info(f"{key}:", value)
