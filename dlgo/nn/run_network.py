# tag::test_setup[]
import load_mnist
import network
from layers import DenseLayer, ActivationLayer
import six.moves.cPickle as pickle
import gzip

training_data, test_data = load_mnist.load_data()  # <1>

net = network.SequentialNetwork()  # <2>

net.add(DenseLayer(784, 392))  # <3>
net.add(ActivationLayer(392))
net.add(DenseLayer(392, 196))
net.add(ActivationLayer(196))
net.add(DenseLayer(196, 98))
net.add(ActivationLayer(98))
net.add(DenseLayer(98, 10))
net.add(ActivationLayer(10))  # <4>

# <1> First, load training and test data.
# <2> Next, initialize a sequential neural network.
# <3> You can then add dense and activation layers one by one.
# <4> The final layer has size 10, the number of classes to predict.
# end::test_setup[]
# tag::test_run[]

with gzip.open('mine.pkl.gz', 'rb') as f:
    raw_class_train_data, raw_class_test_data = pickle.load(f)
class_test_data = load_mnist.shape_data(raw_class_test_data)

net.train(training_data, epochs=10, mini_batch_size=10,
          learning_rate=3.0, inner_test_data=test_data, test_data=class_test_data)  # <1>

# <1> You can now easily train the model by specifying train and test data, the number of epochs, the mini-batch size and the learning rate.
# end::test_run[]
