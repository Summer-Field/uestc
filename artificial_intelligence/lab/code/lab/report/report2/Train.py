import models

FILE = '../data_banknote_authentication.txt'

SVC = models.SVM_model(FILE)
LR = models.LR(FILE)
MLP = models.DeepLearning(FILE)
MY = models.MyCNN(FILE)

# SVC
SVC.train()
SVC.evaluate()

# LR
LR.train()
LR.evaluate()

# DeepLearning
MLP.build_model()
MLP.train()

# MyCNN
MY.build_model()
MY.train()