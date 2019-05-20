from tflearn.data_preprocessing import ImagePreprocessing
import tflearn

def build_net():

    n = 5

    tflearn.config.init_training_mode()

    img_prep = ImagePreprocessing()
    img_prep.add_featurewise_zero_center()
    img_prep.add_featurewise_stdnorm()

    # Real-time data augmentation
    img_aug = tflearn.ImageAugmentation()
    img_aug.add_random_flip_leftright()
    # img_aug.add_random_crop([48, 48], padding=8)

    # Building Residual Network
    net = tflearn.input_data(shape=[None, 48, 48, 1], data_preprocessing=img_prep, data_augmentation=img_aug)
    net = tflearn.conv_2d(net, nb_filter=16, filter_size=3, regularizer='L2', weight_decay=0.0001)
    net = tflearn.residual_block(net, n, 16)
    net = tflearn.residual_block(net, 1, 32, downsample=True)
    net = tflearn.residual_block(net, n - 1, 32)
    net = tflearn.residual_block(net, 1, 64, downsample=True)
    net = tflearn.residual_block(net, n - 1, 64)
    net = tflearn.batch_normalization(net)
    net = tflearn.activation(net, 'relu')
    net = tflearn.global_avg_pool(net)

    # Regression
    net = tflearn.fully_connected(net, 7, activation='softmax')
    mom = tflearn.Momentum(learning_rate=0.1, lr_decay=0.0001, decay_step=32000, staircase=True, momentum=0.9)
    net = tflearn.regression(net, optimizer=mom,
                             loss='categorical_crossentropy')
    print("make model")
    model = tflearn.DNN(net, checkpoint_path='upload/Resmodels/model_resnet_emotion',
                        max_checkpoints=10, tensorboard_verbose=0, clip_gradients=0.)
    print("load model start")
    model.load('upload/Resmodels/model_resnet_emotion-10500')
    print("load model success")

    return model


