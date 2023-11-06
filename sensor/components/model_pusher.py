import sys

from sensor.entity.artifact_entity import ModelPusherArtifact, ModelTrainerArtifact
from sensor.entity.config_entity import ModelPusherConfig
from sensor.exception import SensorException
from sensor.logger import logging
#from sensor.ml.model.s3_estimator import SensorEstimator
import os


from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.artifact_entity import ModelPusherArtifact,ModelTrainerArtifact,ModelEvaluationArtifact
from sensor.entity.config_entity import ModelEvaluationConfig,ModelPusherConfig
import os,sys
from sensor.ml.metric.classification_metric import get_classification_score
from sensor.utils.main_utils import save_object,load_object,write_yaml_file
import shutil

class ModelPusher:

    def __init__(self,
                 model_pusher_config:ModelPusherConfig,
                 model_evaluation_artifact:ModelEvaluationArtifact) -> ModelPusherArtifact:
        
        try:
            self.model_pusher_config = model_pusher_config
            self.model_evaluation_artifact = model_evaluation_artifact

        except Exception as e:
            raise SensorException(e, sys)
        
    def initiate_model_pusher(self) -> ModelPusherArtifact:
        try:
            # Get trained model file path
            trained_model_path = self.model_evaluation_artifact.trained_model_path
            
            # Creating model pusher dir
            model_file_path = self.model_pusher_config.model_file_path
            os.makedirs(os.path.dirname(model_file_path), exist_ok=True)
            shutil.copy(src=trained_model_path, dst=model_file_path)

            # Saved model directory
            saved_model_path = self.model_pusher_config.saved_model_path
            os.makedirs(os.path.dirname(saved_model_path), exist_ok=True)
            shutil.copy(src=trained_model_path, dst=saved_model_path)

            # Model pusher artifact
            model_pusher_artifact = ModelPusherArtifact(saved_model_path=saved_model_path,
                                                        model_file_path=model_file_path)
            logging.info("Model copied successfully")
            logging.info(f"Model pusher artifact: {model_pusher_artifact}")
            return model_pusher_artifact

        except Exception as e:
            raise SensorException(e, sys)
