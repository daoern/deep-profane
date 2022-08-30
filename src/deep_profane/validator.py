from src.deep_profane import tfhub_bert_handle
from src.deep_profane import model_weights

# deep learning
import tensorflow as tf
import tensorflow_text as text
import tensorflow_hub as hub
from keras.layers import Dense

class ProfanityValidator:
    def __init__(self):
        print("Building model...")

        self.model = self.build_classifier_model('small_bert/bert_en_uncased_L-4_H-512_A-8')

        print("Loading weights...")
        weight = model_weights.fetch_weights('small-bert')
        self.model.load_weights(weight)
        
        print("Model initialized!")


    def build_classifier_model(self, bert_model_name):
        text_input = tf.keras.layers.Input(shape=(), dtype=tf.string, name='text')
        preprocessing_layer = hub.KerasLayer(tfhub_bert_handle.preprocess[bert_model_name], name='preprocessing')
        encoder_inputs = preprocessing_layer(text_input)
        encoder = hub.KerasLayer(tfhub_bert_handle.encoder[bert_model_name], trainable=False, name='BERT_encoder')
        outputs = encoder(encoder_inputs)
        net = outputs['pooled_output']

        net = tf.keras.layers.Lambda(lambda x: tf.stop_gradient(x))(net)

        net = Dense(512, activation='relu')(net)
        net = tf.keras.layers.Dropout(0.1)(net)
        net = tf.keras.layers.Dense(1, activation='sigmoid', name='classifier')(net)
        return tf.keras.Model(text_input, net)
    
    def get_profane_prob(self, texts):
        return self.model.predict(tf.constant(texts)).ravel()

    def is_profane(self, texts):
        return (self.get_profane_prob(texts) > 0.5).astype(bool)
