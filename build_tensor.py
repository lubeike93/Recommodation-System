from keras.models import load_model
from user_character_generation import character_of_the_user_in_comment, Y
from sight_character_generation import character_of_the_post_in_comment
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

X = np.hstack((character_of_the_post_in_comment, character_of_the_user_in_comment))

def build_linear_model(input_dim):
    # create model
    model = Sequential()
    model.add(Dense(60, input_dim = input_dim, kernel_initializer='normal', activation='relu'))
    model.add(Dense(40, activation='relu'))
    model.add(Dense(30, activation='relu'))
    model.add(Dense(1, kernel_initializer='normal', activation='sigmoid'))
    # Compile model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


def fit_linear_model(X_train, y_train, dimension, iteration, loadfile=None, savefile=None):
    if iteration == 0:
        return load_model(loadfile)
    if loadfile is None:
        model = build_linear_model(dimension)
    else:
        model = load_model(loadfile)
    model.fit(X_train, y_train, nb_epoch=iteration, verbose=1, batch_size=64)

    return model


def main():

    train_x, test_x, train_y, test_y = train_test_split(X, Y, test_size=0.2)
    sc = StandardScaler()
    train_x = sc.fit_transform(train_x)
    test_x = sc.transform(test_x)

    model = fit_linear_model(X_train=train_x,
                             y_train=train_y,
                             dimension=X.shape[1],
                             iteration=3500,
                             loadfile=None)
    y_out = model.predict(test_x)
    y_out_train = model.predict(train_x)
    print(train_y)
    print(y_out_train)
    prediction_labels = np.argmax(y_out, axis=1)
    #print(prediction_labels)


if __name__ == "__main__":
    main()
