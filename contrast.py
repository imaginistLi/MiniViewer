# -*- coding: utf-8 -*-
# ===========
# Author: imaginist_Lee
# Email: imaginist@sjtu.edu.cn
# ===========


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
import numpy as np
import cv2


class Ui_MiniViewer(QtWidgets.QWidget):
    def __init__(self):
        super(Ui_MiniViewer, self).__init__()
        self.data_path = ''
        self.label_path = ''
        self.pred_path = ''
        self.image_data = None
        self.label_data = None
        self.pred_data = None
        self.image_load_flag = False
        self.label_load_flag = False
        self.pred_load_flag = False

        self.index = 0

        self.InitUI()
        self.set_signals()


    def InitUI(self):
        self.setObjectName("MiniViewer")
        self.setWindowIcon(QtGui.QIcon('images/sasuke.jpg'))
        self.resize(344, 88)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.load_images_bn = QtWidgets.QPushButton(self)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.load_images_bn.setFont(font)
        self.load_images_bn.setObjectName("load_images_bn")
        self.verticalLayout.addWidget(self.load_images_bn)
        self.load_preds_bn = QtWidgets.QPushButton(self)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.load_preds_bn.setFont(font)
        self.load_preds_bn.setObjectName("load_preds")
        self.verticalLayout.addWidget(self.load_preds_bn)
        self.load_labels_bn = QtWidgets.QPushButton(self)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.load_labels_bn.setFont(font)
        self.load_labels_bn.setObjectName("load_labels")
        self.verticalLayout.addWidget(self.load_labels_bn)
        self.position = QtWidgets.QLabel(self)
        self.position.setFont(font)
        self.position.setText("index:")
        self.position.setObjectName("position")
        self.verticalLayout.addWidget(self.position)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.image_label = QtWidgets.QLabel(self)
        self.image_label.setText("")
        self.image_label.setObjectName("image_label")
        self.horizontalLayout.addWidget(self.image_label)
        self.pred_label = QtWidgets.QLabel(self)
        self.pred_label.setText("")
        self.pred_label.setObjectName("pred_label")
        self.horizontalLayout.addWidget(self.pred_label)
        self.mask_label = QtWidgets.QLabel(self)
        self.mask_label.setText("")
        self.mask_label.setObjectName("mask_label")
        self.horizontalLayout.addWidget(self.mask_label)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi()


    def set_signals(self):
        QtCore.QMetaObject.connectSlotsByName(self)
        self.load_images_bn.clicked.connect(self.open_img_file)
        self.load_labels_bn.clicked.connect(self.open_label_file)
        self.load_preds_bn.clicked.connect(self.open_pred_file)


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MiniViewer", "MiniViewer"))
        self.load_images_bn.setText(_translate("MiniViewer", "load images"))
        self.load_labels_bn.setText(_translate("MiniViewer", "load labels"))
        self.load_preds_bn.setText(_translate("MiniViewer", "load preds"))


    def draw_contours(self, img):
        # draw label
        if self.label_load_flag:
            if self.image_data.shape[0] == self.label_data.shape[0]:
                if self.label_data[self.index].sum() != 0:
                    label_slice = self.label_data[self.index].astype(np.uint8)
                    _, contours_label, _ = cv2.findContours(label_slice, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                    img = cv2.drawContours(img, contours_label, -1, (255, 132, 124), -1)
        # draw predicted result
        if self.pred_load_flag:
            if self.image_data.shape[0] == self.pred_data.shape[0]:
                if self.pred_data[self.index].sum() != 0:
                    pred_slice = self.pred_data[self.index].astype(np.uint8)
                    _, contours_pred, _ = cv2.findContours(pred_slice, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                    img = cv2.drawContours(img, contours_pred, -1, (168, 255, 101), -1)

        myqimage = QtGui.QImage(img, img.shape[1], img.shape[0], img.strides[0], QtGui.QImage.Format_RGB888)
        self.image_label.setPixmap(QtGui.QPixmap.fromImage(myqimage))


    def open_img_file(self):
        dataName, dataType = QFileDialog.getOpenFileName(self, "open images", self.data_path, " *.npy")
        if dataName:
            self.data_path = dataName
            print(dataName)
            self.index = 0
            self.position.setText('index: %d'% (self.index + 1))
            self.image_data = np.load(dataName)
            self.image_data[self.image_data < -100] = -100
            self.image_data[self.image_data > 240] = 240
            print("self.image_data.shape:", self.image_data.shape)
            self.image_load_flag = True
            # show image
            self.img_refresh()

    def img_refresh(self):
        temp_image = self.image_data[self.index]
        img = np.copy(temp_image)
        img = np.uint8((img - img.min()) / img.ptp() * 255.0)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        self.draw_contours(img)


    def open_label_file(self):
        dataName, dataType = QFileDialog.getOpenFileName(self, "open labels", self.label_path, " *.npy")
        if dataName:
            self.label_path = dataName
            print(dataName)
            self.label_data = np.load(dataName, allow_pickle=True)
            print("self.label_data.shape:", self.label_data.shape)
            self.label_load_flag = True
            self.img_refresh()
            # show image
            self.label_refresh()

    def label_refresh(self):
        if self.label_load_flag and self.image_data.shape[0] == self.label_data.shape[0]:
            temp_image = self.label_data[self.index]
            img = np.copy(temp_image).astype(np.float)
            img = np.uint8((img - img.min()) / img.ptp() * 255.0)
            myqimage = QtGui.QImage(img, img.shape[1], img.shape[0], img.strides[0], QtGui.QImage.Format_Indexed8)
            self.mask_label.setPixmap(QtGui.QPixmap.fromImage(myqimage))

    def open_pred_file(self):
        dataName, dataType = QFileDialog.getOpenFileName(self, "open preds", self.pred_path, " *.npy")
        if dataName:
            self.pred_path = dataName
            print(dataName)
            self.pred_data = np.load(dataName, allow_pickle=True)
            self.pred_data = self.pred_data > 0.5  # binarization
            print("self.label_data.shape:", self.pred_data.shape)
            self.pred_load_flag = True
            self.img_refresh()
            # show image
            self.label_refresh()
            self.pred_refresh()

    def pred_refresh(self):
        if self.pred_load_flag and self.image_data.shape[0] == self.pred_data.shape[0]:
            temp_image = self.pred_data[self.index]
            img = np.copy(temp_image).astype(np.float)
            img = np.uint8((img - img.min()) / img.ptp() * 255.0)
            myqimage = QtGui.QImage(img, img.shape[1], img.shape[0], img.strides[0], QtGui.QImage.Format_Indexed8)
            self.pred_label.setPixmap(QtGui.QPixmap.fromImage(myqimage))

    def wheelEvent(self, event):
        if self.image_load_flag or self.label_load_flag:
            self.index = (self.index - event.angleDelta().y() // 120) % self.image_data.shape[0]
            self.position.setText('index: %d' % (self.index + 1))
        if self.image_load_flag:
            self.img_refresh()
        if self.label_load_flag:
            self.label_refresh()
        if self.pred_load_flag:
            self.pred_refresh()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MiniViewer()
    ui.show()
    sys.exit(app.exec_())