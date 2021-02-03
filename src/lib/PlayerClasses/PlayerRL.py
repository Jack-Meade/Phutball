from   .Player     import Player
import keras
import numpy       as     np
import tensorflow  as     tf
from   collections import deque
from   copy        import deepcopy
from   itertools   import chain
from   pathlib     import Path

class PlayerRL(Player):
    def __init__(self, board):
        self._input_shape     = len(board.state)*len(board.state[0])
        self._num_outputs     = 1
        self._replay_buffer   = deque(maxlen=2000)
        self._batch_size      = 64
        self._discount_factor = 0.95
        self._optimizer       = keras.optimizers.Adam(lr=1e-3)
        self._loss_fn         = keras.losses.mean_squared_error
        self._model_src       = f"{Path(__file__).parent.parent}/models/model{self._input_shape}"
        try:
            self._model   = keras.models.load_model(self._model_src, compile=False)
            self._trained = True
        except OSError:
            self._model   = keras.models.Sequential([
                keras.layers.Dense(64, activation="elu", input_dim=self._input_shape),
                keras.layers.Dense(32, activation="elu"),
                keras.layers.Dense(self._num_outputs)
            ])
            self._trained = False

    def take_turn(self, board, p1, depth, heuristic, abp):
        if not self._trained:
            self.train(board, p1)
            self._trained = True
        return self.play_one_step(board, 0, p1)[0]

    def train(self, board, p1):
        original = deepcopy(board)
        episodes = 300
        for episode in range(episodes):
            board = deepcopy(original)
            for step in range(200):
                epsilon = 0.5
                board, done = self.play_one_step(board, epsilon, p1)
                if done: break
            if episode > self._batch_size:
                self.training_step()
            if episode % 5 == 0: print(f"finished episode {episode}/{episodes}")
        self._model.save(self._model_src)

    def play_one_step(self, board, epsilon, p1):
        next_state, reward, done = self.epsilon_greedy_policy(board, epsilon, p1)
        self._replay_buffer.append((board, reward, next_state, done))
        return next_state, done

    def epsilon_greedy_policy(self, board, epsilon, p1):
        next_states = board.get_successors()

        if np.random.rand() < epsilon:
            action = np.random.randint(len(next_states)-1)
        else:
            qvalues = []
            for state in next_states:
                qvalues.append(self._model.predict(self.flatten(state)))
            action = np.argmax(qvalues)

        return self.step(action, next_states, p1)    

    def step(self, action, next_states, p1):
        new_state = next_states[action]

        if 1 in new_state.state[0] or 1 in new_state.state[1]:
            if p1: return new_state, -1, True
            else:  return new_state,  1, True
        if 1 in new_state.state[len(new_state)-1] or 1 in new_state.state[len(new_state)-2]:
            if p1: return new_state,  1, True
            else:  return new_state, -1, True
        
        return new_state, 0, False

    def sample_experiences(self):
        indices = np.random.randint(len(self._replay_buffer), size=self._batch_size)
        batch   = [self._replay_buffer[index] for index in indices]
        states, rewards, next_states, dones = [
            np.array([experience[field_index] for experience in batch]) 
            for field_index in range(4)
        ]
        return states, rewards, next_states, dones

    def training_step(self):
        states, rewards, next_states, dones = self.sample_experiences()

        next_q_values = []
        for next_state in next_states:
            next_q_values.append(self._model.predict(self.flatten(next_state)))
        
        max_next_q_values = np.max(next_q_values)
        target_q_values   = (rewards + (1 - dones) * self._discount_factor * max_next_q_values)

        with tf.GradientTape() as tape:
            all_q_values = [self._model(self.flatten(state)) for state in states]
            q_values     = tf.reduce_sum(all_q_values)
            loss         = tf.reduce_mean(self._loss_fn(target_q_values, q_values))

            grads = tape.gradient(loss, self._model.trainable_variables)
            self._optimizer.apply_gradients(zip(grads, self._model.trainable_variables))

    def flatten(self, state):
        return np.array(list(chain.from_iterable(state.state))).reshape(-1, self._input_shape)