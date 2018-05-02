
import numpy as np
import tensorflow as tf

class Agent():
	def __init__(self, building_height, elevator_nums, actions):

		self.gamma = .99               # discount factor for reward
		self.decay = 0.99    

		self.elevator_nums = elevator_nums
		self.actions = actions

		self.batch_size = 32
		self.input_shape = [None, building_height+2*elevator_nums]
		self.action_num = self.elevator_nums*actions#self.elevator_nums*self.actions
		
		self.learning_rate = 0.001
		self.momentum = 0.9

		self.graphpath = "./graphs"
		self.modelpath = "./models"

		self.build_model()
		self.build_loss()

		self.summary = tf.summary.merge([self.loss_graph])

		self.sess = tf.InteractiveSession()
		self.sess.run(tf.global_variables_initializer())

		self.writer = tf.summary.FileWriter(self.graphpath, self.sess.graph)
		self.saver = tf.train.Saver()

	def get_action(self, state):
		output = self.sess.run(self.out_actions, feed_dict={self.input_state: state})
		actions = []
		for idx in range(self.elevator_nums):
			actions.append(np.random.choice(self.actions, p=output[0][idx]))

		return actions

	def update_network(self, states, actions, advantages, counter):
		batch_feed = {self.input_state: states,
					  self.input_act: actions,
					  self.input_adv: advantages}

		loss, summary, _ = self.sess.run([self.loss, self.summary, self.trainer], feed_dict=batch_feed)
		self.writer.add_summary(summary, counter)

		return loss

	def build_model(self):
		self.input_state = tf.placeholder(tf.float32, shape=self.input_shape)
		self.input_act = tf.placeholder(tf.int32, shape=[None, 1])
		self.input_adv = tf.placeholder(tf.float32, shape=[None, 1])

		self.logit, self.out_actions = self.Policy_Network(self.input_state)

		self.trainable_vars = tf.trainable_variables()

	
	def build_loss(self):
		def tf_discount_rewards(tf_r): #tf_r ~ [game_steps,1]
		    discount_f = lambda a, v: a*self.gamma + v;
		    tf_r_reverse = tf.scan(discount_f, tf.reverse(tf_r,[True, False]))
		    tf_discounted_r = tf.reverse(tf_r_reverse,[True, False])
		    return tf_discounted_r

		#discount rewards and normalize
		tf_discounted_epr = tf_discount_rewards(self.input_adv)
		tf_mean, tf_variance= tf.nn.moments(tf_discounted_epr, [0], shift=None, name="reward_moments")
		tf_discounted_epr -= tf_mean
		tf_discounted_epr /= tf.sqrt(tf_variance + 1e-6)

		# self.loss = tf.nn.l2_loss(self.input_act - self.actions)
		# self.optimizer = tf.train.RMSPropOptimizer(self.learning_rate, decay=self.decay)
		# tf_grads = self.optimizer.compute_gradients(self.loss, var_list=tf.trainable_variables(), grad_loss=tf_discounted_epr)
		# self.train = self.optimizer.apply_gradients(tf_grads)


		#Another version 
		log_prob = tf.log(tf.clip_by_value(self.out_actions,1e-10,1.0))
		indices = tf.range(0, tf.shape(log_prob)[0]) * tf.shape(log_prob)[1] + self.input_act
		act_prob = tf.gather(tf.reshape(log_prob, [-1]), indices)

		self.loss = -tf.reduce_sum(tf.multiply(act_prob, tf_discounted_epr))
		
		optimizer = tf.train.RMSPropOptimizer(self.learning_rate)
		self.trainer = optimizer.minimize(self.loss)


		self.loss_graph = tf.summary.scalar("loss", self.loss)


		print "Created loss ..."


	def Policy_Network(self, input, name="policy_network"):

		with tf.variable_scope(name): 
			fc1 = tf.contrib.layers.fully_connected(input, 1024,
													activation_fn=tf.nn.relu,
													scope='fc1')

			fc2 = tf.contrib.layers.fully_connected(fc1, 512, 
													activation_fn=tf.nn.relu,
													scope='fc2')

			fc3 = tf.contrib.layers.fully_connected(fc2, 256, 
													activation_fn=tf.nn.relu,
													scope='fc3')

			fc4 = tf.contrib.layers.fully_connected(fc3, self.action_num, 
													activation_fn=None,
													scope='fc4')		

			fc4 = tf.reshape(fc4, [-1, self.elevator_nums, self.actions])

			#implement fc layer
			output = tf.nn.softmax(fc4, dim=2)

			return fc4, output

	def save(self, num):
		save_path = self.saver.save(self.sess, self.modelpath + "slingshotmodel", global_step=num)

	def reload(self):
		latest_chkpt_path = tf.train.latest_checkpoint(self.modelpath)
		self.saver.restore(self.sess, latest_chkpt_path)
		print 'Reloaded model : ' + latest_chkpt_path

		game_steps = int(latest_chkpt_path.split('-')[1])
		return game_steps
