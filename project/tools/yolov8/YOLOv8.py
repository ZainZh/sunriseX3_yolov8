import time
import cv2
import numpy as np
try:
    import onnxruntime as onnxruntime
except ImportError:
    onnxruntime =None
from .utils import xywh2xyxy, draw_detections, multiclass_nms, bgr2nv12_opencv
from common import print_info
try:
    from hobot_dnn import pyeasy_dnn as dnn
except ImportError:
    dnn = None


class YOLOv8:
    def __init__(
            self, conf_thres=0.7, iou_thres=0.5, input_shape: list = (1, 3, 640, 640)
    ):
        self.conf_threshold = conf_thres
        self.iou_threshold = iou_thres

        self.boxes, self.scores, self.class_ids = [], [], []
        self.img_height, self.img_width = 0, 0
        self.input_height, self.input_width = input_shape[2], input_shape[3]

    def detect_objects(self, image):
        input_tensor = self.prepare_input(image)

        # Perform inference on the image
        outputs = self.inference(input_tensor)
        print(outputs[0])
        self.boxes, self.scores, self.class_ids = self.process_output(outputs)

        return self.boxes, self.scores, self.class_ids

    def prepare_input(self, image):
        raise NotImplementedError

    def inference(self, input_tensor):
        raise NotImplementedError

    def process_output(self, output):
        predictions = np.squeeze(output[0]).T
        print("predictions shape is",predictions.shape)
        # Filter out object confidence scores below threshold
        scores = np.max(predictions[:, 4:], axis=1)
        predictions = predictions[scores > self.conf_threshold, :]
        scores = scores[scores > self.conf_threshold]

        if len(scores) == 0:
            return [], [], []

        # Get the class with the highest confidence
        class_ids = np.argmax(predictions[:, 4:], axis=1)

        # Get bounding boxes for each object
        boxes = self.extract_boxes(predictions)

        # Apply non-maxima suppression to suppress weak, overlapping bounding boxes
        # indices = nms(boxes, scores, self.iou_threshold)
        indices = multiclass_nms(boxes, scores, class_ids, self.iou_threshold)

        return boxes[indices], scores[indices], class_ids[indices]

    def extract_boxes(self, predictions):
        # Extract boxes from predictions
        boxes = predictions[:, :4]

        # Scale boxes to original image dimensions
        boxes = self.rescale_boxes(boxes)

        # Convert boxes to xyxy format
        boxes = xywh2xyxy(boxes)

        return boxes

    def rescale_boxes(self, boxes):
        # Rescale boxes to original image dimensions
        input_shape = np.array(
            [self.input_width, self.input_height, self.input_width, self.input_height]
        )
        boxes = np.divide(boxes, input_shape, dtype=np.float32)
        boxes *= np.array(
            [self.img_width, self.img_height, self.img_width, self.img_height]
        )
        return boxes

    def draw_detections(self, image, draw_scores=True, mask_alpha=0.4):
        return draw_detections(
            image, self.boxes, self.scores, self.class_ids, mask_alpha
        )


class YOLOv8ONNX(YOLOv8):
    def __init__(self, model, conf_thres=0.7, iou_thres=0.5):
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

        super().__init__(conf_thres=conf_thres, iou_thres=iou_thres, input_shape=self.input_shape)

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

    # def prepare_input(self, image):
    #     self.img_height, self.img_width = image.shape[:2]
    #
    #     input_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #
    #     # Resize input image
    #     input_img = cv2.resize(input_img, (self.input_width, self.input_height))
    #     input_img = bgr2nv12_opencv(input_img)
    #
    #     return input_img


    def inference(self, input_tensor):
        start = time.perf_counter()
        outputs = self.session.run(
            self.output_names, {self.input_names[0]: input_tensor}
        )

        print(f"Inference time: {(time.perf_counter() - start) * 1000:.2f} ms")
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


class YOLOv8BIN(YOLOv8):
    def __init__(self, model, conf_thres=0.7, iou_thres=0.5):
        self.model = dnn.load(str(model))
        self.model_input_properties = self.model[0].inputs[0].properties
        self.model_output_properties = self.model[0].outputs[0].properties

        # get input details
        self.input_shape =  self.model_input_properties.shape    # get output details
        self.output_shape = self.model_output_properties.shape

        print("model_input_properties:===============")
        self.print_model_info(self.model_input_properties)
        print("model_output_properties:===============")
        self.print_model_info(self.model_output_properties)

        super().__init__(conf_thres=conf_thres, iou_thres=iou_thres, input_shape=self.input_shape)

    def __call__(self, image):
        return self.detect_objects(image)

    def inference(self, input_tensor):
        start = time.perf_counter()
        outputs = self.model[0].forward(input_tensor)
        print(f"Inference time: {(time.perf_counter() - start) * 1000:.2f} ms")
        return outputs

    # def prepare_input(self, image):
    #     self.img_height, self.img_width = image.shape[:2]
    #
    #     input_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #
    #     # Resize input image
    #     input_img = cv2.resize(input_img, (self.input_width, self.input_height))
    #
    #     # Scale input pixel values to 0 to 1
    #     input_img = input_img / 255.0
    #     input_img = input_img.transpose(2, 0, 1)
    #     input_tensor = input_img[np.newaxis, :, :, :].astype(np.float32)
    #
    #     return input_tensor

    def prepare_input(self, image):
        self.img_height, self.img_width = image.shape[:2]
        # Resize input image
        input_img = cv2.resize(image, (self.input_width, self.input_height))
        input_img = bgr2nv12_opencv(input_img)
        # Scale input pixel values to 0 to 1

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


