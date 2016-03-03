import sys
from PyQt4 import QtGui
import matplotlib.pyplot as plt
import DistributionGenerator

class Example(QtGui.QWidget):

    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        self.resize(250, 150)
        #self.center()
        self.setWindowTitle('Center')

        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        btn = QtGui.QPushButton('Generate Jobs', self)
        btn.setToolTip('Click to generate and plot jobs according to the configuration fields')
        btn.resize(btn.sizeHint())
        btn.move(self.width()/2, self.height()/2)
        #btn.clicked.connect(self.generateJobs)

        self.show()
        self.generateJobs()

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def generateJobs(self):
        gen = DistributionGenerator.DistributionGenerator()
        r = gen.generateJobs(2000,'normal')
        #fig, ax = plt.subplots(1,1)
        plt.hist(r, normed=True)
        #plt.ioff()
        #plt.draw()
        plt.show()

def main():

    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()