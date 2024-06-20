from environment import *
from models import *
import time

#new_model = BasicModel(0.01)
#new_model.learning_rate = 0.5

environment = Environment('neural_network_model.keras', new_run=True)

start_time = time.time()
environment.run(1000)
print(f"{time.time()-start_time} seconds")

# from environment import Environment
# import time

# new_model = BasicModel(0.01)
# new_model.learning_rate = 0.5
# environment = Environment('test_basic_model_2.p', new_run=True)

# start_time = time.time()
# environment.run(100)
# print(f"{time.time() - start_time} seconds")
