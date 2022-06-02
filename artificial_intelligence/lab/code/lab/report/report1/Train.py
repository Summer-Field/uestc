import models

FILE = '../quake.dat'

LR_model = models.LR(FILE)
SVM_rbf = models.SVM_model_rbf(FILE)
SVM_linear = models.SVM_model_linear(FILE)
MLP = models.DeepLearning(FILE)

LR_model.train()
LR_model.evaluate()
print('\n')
SVM_rbf.train()
SVM_rbf.evaluate()
print('\n')
SVM_linear.train()
SVM_linear.evaluate()
print('\n')
MLP.build_model()
MLP.train()
