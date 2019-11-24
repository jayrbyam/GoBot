import h5py

from dlgo.agent.predict import DeepLearningAgent, load_prediction_agent
from dlgo.data.parallel_processor import GoDataProcessor
from dlgo.encoders.sevenplane import SevenPlaneEncoder

from dlgo.httpfrontend.server import get_web_app
from keras.models import Sequential
from keras.layers import Dense
from dlgo.networks import large

if __name__ == '__main__': 
    go_board_rows, go_board_cols = 19, 19
    num_classes = go_board_rows * go_board_cols

    encoder = SevenPlaneEncoder((go_board_rows, go_board_cols))
    processor = GoDataProcessor(encoder = encoder.name())
    X, Y = processor.load_go_data(num_samples=100)

    input_shape = (encoder.num_planes, go_board_rows, go_board_cols)
    model = Sequential()
    network_layers = large.layers(input_shape)
    for layer in network_layers:
        model.add(layer)
    model.add(Dense(num_classes, activation = 'softmax'))
    model.compile(loss = 'categorical_crossentropy', optimizer = 'adadelta', metrics = ['accuracy'])

    model.fit(X, Y, batch_size = 128, epochs = 20)
    model.save("deep_bot.h5")

    model_file = h5py.File("deep_bot.h5", "w")
    deep_learning_bot = DeepLearningAgent(model, encoder)
    deep_learning_bot.serialize(model_file)
