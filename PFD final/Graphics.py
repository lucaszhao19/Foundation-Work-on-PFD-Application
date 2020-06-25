from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QTextDocument , QTextCursor ,QTextCharFormat ,QFont ,QPixmap, QCursor, QTransform, QColor
from PyQt5.uic import loadUiType
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsProxyWidget, QGraphicsObject, QGraphicsEllipseItem ,QGraphicsPixmapItem,QApplication, QGraphicsView, QGraphicsScene, QHBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QPolygonF, QBrush ,QTransform ,QMouseEvent, QIcon, QPainter
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtSvg import QGraphicsSvgItem, QSvgWidget, QSvgRenderer

from functools import partial
from collections import defaultdict
import sys
import math

class Graphics(QtWidgets.QGraphicsItem):
    flag = True

    def __init__(self):
        QtWidgets.QGraphicsItem.__init__(self)
        self.scene = QGraphicsScene()
        self.scene.setItemIndexMethod(QGraphicsScene.BspTreeIndex)
        # self.pos = None
    
    def getScene(self):
        return self.scene

    def createNodeItem(self,unitOpType, graphicsView):
        return NodeItem(unitOpType, graphicsView)
    
class NodeAnchor(QtWidgets.QGraphicsItem):
    
    def __init__(self, parent, index):
        super(NodeAnchor, self).__init__(parent)
        self.pos = QtCore.QPointF(0,0)
        self.rect = QRectF(self.pos.x(), self.pos.y(),4,4)
        self.typee = 'Graphics.NodeAnchor'
        self.parent = parent
        self.index = index
        self.flagg = True
        self.setAcceptHoverEvents(True)
        self.setParentItem(self.parent)
        # self.setZValue(1000)
        self.setFlag(QGraphicsItem.ItemIsMovable)
    
        # Brush.
        self.brush = QtGui.QBrush()
        self.brush.setStyle(QtCore.Qt.SolidPattern)
        self.brush.setColor(QtGui.QColor(220,220,220,255))  
        # Pen.
        self.pen = QtGui.QPen()
        self.pen.setStyle(QtCore.Qt.SolidLine)
        self.pen.setWidth(1)
        self.pen.setColor(QtGui.QColor(20,20,20,255)) 

    def shape(self):
        path = QtGui.QPainterPath()
        path.addEllipse(self.boundingRect())
        return path
 
    def boundingRect(self):
        return QtCore.QRectF(self.rect)
 
    def paint(self, painter, option, widget):
        painter.setPen(self.pen)
        painter.drawEllipse(QtCore.QRectF(self.rect))

    def mousePressEvent(self, event):
        super(NodeAnchor, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.pos = QPointF(event.scenePos())
        self.parent.flaggg = False

        if self.parent.pointB.x() - self.parent.pointA.x() < 30:
            if self.index == 1:
                line1 = self.parent.line1.line()
                line2 = self.parent.line2.line()
                line3 = self.parent.line3.line()
                self.parent.line1.setLine(line1.x1(), line1.y1(), self.pos.x(), line1.y2())
                self.parent.line2.setLine(self.pos.x(), line1.y1(), self.pos.x(), line2.y2())
                self.parent.line3.setLine(self.pos.x(), line2.y2(), line3.x2(), line3.y2())
                  
                self.parent.anchor1Pos = QPointF(self.parent.line2.line().x1(), (self.parent.line2.line().y1()+self.parent.line2.line().y2())/2)
            elif self.index == 2:
                line2 = self.parent.line2.line()
                line3 = self.parent.line3.line()
                line4 = self.parent.line4.line()
                self.parent.line2.setLine(line2.x1(), line2.y1(), line2.x2(), self.pos.y())
                self.parent.line3.setLine(line2.x2(), self.pos.y(), line3.x2(), self.pos.y())
                self.parent.line4.setLine(line3.x2(), self.pos.y(), line4.x2(), line4.y2())
                    
                self.parent.anchor2Pos = QPointF((self.parent.line3.line().x1()+self.parent.line3.line().x2())/2, self.parent.line3.line().y1())
            elif self.index == 3:
                line3 = self.parent.line3.line()
                line4 = self.parent.line4.line()
                line5 = self.parent.line5.line()
                self.parent.line3.setLine(line3.x1(), line3.y1(), self.pos.x(), line3.y2())
                self.parent.line4.setLine(self.pos.x(), line3.y2(), self.pos.x(), line4.y2())
                self.parent.line5.setLine(self.pos.x(), line4.y2(), line5.x2(), line5.y2())
                  
                self.parent.anchor3Pos = QPointF(self.parent.line4.line().x1(), (self.parent.line4.line().y1()+self.parent.line4.line().y2())/2)
        else:
            line1 = self.parent.line1.line()
            line2 = self.parent.line2.line()
            line3 = self.parent.line3.line()
            self.parent.line1.setLine(line1.x1(), line1.y1(), self.pos.x(), line1.y1())
            self.parent.line2.setLine(self.pos.x(), line1.y1(), self.pos.x(), line2.y2())
            self.parent.line3.setLine(self.pos.x(), line2.y2(), line3.x2(), line3.y2())
               
            self.parent.anchor1Pos = QPointF(self.parent.line2.line().x1(), (self.parent.line2.line().y1()+self.parent.line2.line().y2())/2)


     
        super(NodeAnchor, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.index == 1:
            self.setPos(self.parent.anchor1Pos)
            # self.parent.anchor2.setPos(self.parent.anchor2Pos)
            # self.parent.anchor3.setPos(self.parent.anchor3Pos)
        elif self.index == 2:
            self.setPos(self.parent.anchor2Pos)
            # self.parent.anchor1.setPos(self.parent.anchor1Pos)
            # self.parent.anchor3.setPos(self.parent.anchor3Pos)
        elif self.index == 3:
            self.setPos(self.parent.anchor3Pos)
            # self.parent.anchor1.setPos(self.parent.anchor1Pos)
            # self.parent.anchor2.setPos(self.parent.anchor2Pos)
        super(NodeAnchor, self).mouseReleaseEvent(event) 

    def anchorMoveEvent(self):
        if self.index == 1:
            self.setPos(self.parent.anchor1Pos)
        elif self.index == 2:
            self.setPos(self.parent.anchor2Pos)
        elif self.index == 3:
            self.setPos(self.parent.anchor3Pos)

    def hoverEnterEvent(self, event):
        cursor = QCursor( Qt.CrossCursor )
        QApplication.instance().setOverrideCursor(cursor)
        
    def hoverLeaveEvent(self, event):
        cursor = QCursor( Qt.ArrowCursor )
        QApplication.instance().setOverrideCursor(cursor)
    
    def set_pos(self, point):
        self.pos = point
        # self.setPos(point)
    
lst = []
class NodeLine(QtWidgets.QGraphicsPathItem):

    def __init__(self, pointA, pointB): 
        super(NodeLine, self).__init__()
        self._pointA = pointA
        self._pointB = pointB
        self.typee = 'Graphics.NodeLine'
        self._source = None
        self._target = None
        self.flag = True
        self.flag1 = True
        self.flaggg = True
        self.connection_line = 1
        self.setZValue(-1)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)

        # Pen
        self.pen = QtGui.QPen()
        self.pen.setStyle(QtCore.Qt.SolidLine)
        self.pen.setWidth(2)
        self.pen.setColor(QtGui.QColor(0,0,0,255))

        # Pen when selected 
        self.selPen = QtGui.QPen()
        self.selPen.setStyle(QtCore.Qt.DashDotDotLine)
        self.selPen.setWidth(2)
        self.selPen.setColor(QtGui.QColor(0,0,0,255))

        # Brush.
        self.brush = QtGui.QBrush()
        self.brush.setStyle(QtCore.Qt.SolidPattern)
        self.brush.setColor(QtGui.QColor(0,0,0,255))
        self.anchor1 = NodeAnchor(self, 1) 
        self.anchor2 = NodeAnchor(self, 2)  
        self.anchor3 = NodeAnchor(self, 3)  

        self.line1 = QGraphicsLineItem()
        self.line2 = QGraphicsLineItem()
        self.line3 = QGraphicsLineItem()
        self.line4 = QGraphicsLineItem()
        self.line5 = QGraphicsLineItem()

        self.line1.setFlag(QGraphicsLineItem.ItemIsSelectable)
        self.line2.setFlag(QGraphicsLineItem.ItemIsSelectable)
        self.line3.setFlag(QGraphicsLineItem.ItemIsSelectable)
        self.line4.setFlag(QGraphicsLineItem.ItemIsSelectable)
        self.line5.setFlag(QGraphicsLineItem.ItemIsSelectable)

        self.line1.setPen(self.pen)
        self.line2.setPen(self.pen)
        self.line3.setPen(self.pen)
        self.line4.setPen(self.pen)
        self.line5.setPen(self.pen)

        self.anchor1Pos = None
        self.anchor2Pos = None
        self.anchor3Pos = None

    def init_path(self, connection):
        if connection == 1:
            midptx = 0.5*(self.pointA.x() + self.pointB.x())    

            pt1 = QtCore.QPointF(midptx , self.pointA.y())
            self.line1.setLine(self.pointA.x(), self.pointA.y(), pt1.x(), pt1.y())
            if self.flag:
                self.scene().addItem(self.line1)

            pt2 = QtCore.QPointF(midptx , self.pointB.y())
            self.line2.setLine(pt1.x(), pt1.y(), pt2.x(), pt2.y())
            if self.flag:
                self.scene().addItem(self.line2)

            pos = QPointF(pt1.x(), (pt1.y()+pt2.y())/2)  
            self.anchor1.set_pos(pos)
            self.anchor1Pos = pos
            # self.anchor1.setPos(self.anchor1Pos)
            # self.anchor1.show()

                
            pt3 = QtCore.QPointF(self.pointB.x()-3 , self.pointB.y())
            self.line3.setLine(pt2.x(), pt2.y(), pt3.x(), pt3.y())
            if self.flag:
                self.scene().addItem(self.line3)

            self.line4.setLine(0,0,0,0)
            self.line5.setLine(0,0,0,0)
            self.anchor2.hide()
            self.anchor3.hide()
            self.flag = False 
            
        elif connection == 2:
            pt1 = QtCore.QPointF(self.pointB.x() , self.pointA.y())
            self.line1.setLine(self.pointA.x(), self.pointA.y(), pt1.x(), pt1.y())
            if self.flag:
                self.scene().addItem(self.line1)

            pt2 = QtCore.QPointF(self.pointB.x() , self.pointB.y())
            self.line2.setLine(pt1.x(), pt1.y(), pt2.x(), pt2.y())
            if self.flag:
                self.scene().addItem(self.line2)

            self.line3.setLine(0,0,0,0)
            self.line4.setLine(0,0,0,0)
            self.line5.setLine(0,0,0,0)
            self.anchor1.hide()
            self.anchor2.hide()
            self.anchor3.hide()
            self.flag = False

        elif connection == 3:
            pt1 = QtCore.QPointF(self.pointA.x() , self.pointB.y())
            self.line1.setLine(self.pointA.x(), self.pointA.y(), pt1.x(), pt1.y())
            if self.flag:
                self.scene().addItem(self.line1)

            pt2 = QtCore.QPointF(self.pointB.x() , self.pointB.y())
            self.line2.setLine(pt1.x(), pt1.y(), pt2.x(), pt2.y())
            if self.flag:
                self.scene().addItem(self.line2)

            self.line3.setLine(0,0,0,0)
            self.line4.setLine(0,0,0,0)
            self.line5.setLine(0,0,0,0)
            self.anchor1.hide()
            self.anchor2.hide()
            self.anchor3.hide()
            self.flag = False

        elif connection == 4:
            pt1 = QtCore.QPointF(self.pointA.x() , self.pointB.y())
            self.line1.setLine(self.pointA.x(), self.pointA.y(), pt1.x(), pt1.y())
            if self.flag:
                self.scene().addItem(self.line1)

            pt2 = QtCore.QPointF(self.pointB.x() , self.pointB.y())
            self.line2.setLine(pt1.x(), pt1.y(), pt2.x(), pt2.y())
            if self.flag:
                self.scene().addItem(self.line2)

            self.line3.setLine(0,0,0,0)
            self.line4.setLine(0,0,0,0)
            self.line5.setLine(0,0,0,0)
            self.anchor1.hide()
            self.anchor2.hide()
            self.anchor3.hide()
            self.flag = False

        elif connection == 5:
            pt1 = QtCore.QPointF(self.pointB.x() , self.pointA.y())
            self.line1.setLine(self.pointA.x(), self.pointA.y(), pt1.x(), pt1.y())
            if self.flag:
                self.scene().addItem(self.line1)

            pt2 = QtCore.QPointF(self.pointB.x() , self.pointB.y())
            self.line2.setLine(pt1.x(), pt1.y(), pt2.x(), pt2.y())
            if self.flag:
                self.scene().addItem(self.line2)

            self.line3.setLine(0,0,0,0)
            self.line4.setLine(0,0,0,0)
            self.line5.setLine(0,0,0,0)
            self.anchor1.hide()
            self.anchor2.hide()
            self.anchor3.hide()
            self.flag = False

        elif connection == 6:
            midpty = 0.5*(self.pointA.y() + self.pointB.y())    

            pt1 = QtCore.QPointF(self.pointA.x(), midpty)
            self.line1.setLine(self.pointA.x(), self.pointA.y(), pt1.x(), pt1.y())
            if self.flag:
                self.scene().addItem(self.line1)

            pt2 = QtCore.QPointF(self.pointB.x(), midpty)
            self.line2.setLine(pt1.x(), pt1.y(), pt2.x(), pt2.y())
            if self.flag:
                self.scene().addItem(self.line2)

            pos = QPointF((pt1.x()+pt2.x())/2, pt1.y())  
            # self.anchor1.rect = QRectF(pt2.x()-2, ((pt2.y()+pt1.y())/2)-2, 5,5)
            self.anchor1.set_pos(pos)
            self.anchor1Pos = pos
            # self.anchor1.setPos(self.anchor1Pos)
            # self.anchor1.show()
                
            pt3 = QtCore.QPointF(self.pointB.x() , self.pointB.y())
            self.line3.setLine(pt2.x(), pt2.y(), pt3.x(), pt3.y())
            if self.flag:
                self.scene().addItem(self.line3)

            self.line4.setLine(0,0,0,0)
            self.line5.setLine(0,0,0,0)
            self.anchor2.hide()
            self.anchor3.hide()
            self.flag = False 



    def updatePath(self):
        if self.connection_line == 1:
            if self.pointB.x() < self.anchor1Pos.x():  
            # if self.pointB.x() < self.pointA.x():
                if self.flag1:
                    pt1 = QtCore.QPointF(self.anchor1Pos.x(), self.pointA.y())
                    self.line1.setLine(self.pointA.x(), self.pointA.y(), pt1.x(), pt1.y())
                   
                    pt2 = QtCore.QPointF(self.anchor1Pos.x() , (self.pointA.y()+self.pointB.y())/2)
                    self.line2.setLine(pt1.x(), pt1.y(), pt2.x(), pt2.y())
                   
                    pos = QPointF(pt1.x(), (pt1.y()+pt2.y())/2) 
                    self.anchor1.set_pos(pos)
                    self.anchor1Pos = pos
                    self.anchor1.setPos(self.anchor1Pos)
                    self.anchor1.show()

                
                    pt3 = QtCore.QPointF(self.pointB.x()-13,  (self.pointA.y()+self.pointB.y())/2)
                    self.line3.setLine(pt2.x(), pt2.y(), pt3.x(), pt3.y())

                    pos = QPointF((pt2.x()+pt3.x())/2, pt2.y()) 
                    self.anchor2.set_pos(pos)
                    self.anchor2Pos = pos
                    self.anchor2.setPos(self.anchor2Pos)
                    self.anchor2.show()

                    pt4 = QtCore.QPointF(self.pointB.x()-13, self.pointB.y())
                    self.line4.setLine(pt3.x(), pt3.y(), pt4.x(), pt4.y())
                    self.scene().addItem(self.line4)
                
                    pos = QPointF(pt3.x(), (pt3.y()+pt4.y())/2) 
                    self.anchor3.set_pos(pos)
                    self.anchor3Pos = pos
                    # self.anchor3.rect = QRectF(pt3.x(), (pt3.y()+pt4.y())/2, 5, 5)
                    self.anchor3.setPos(self.anchor3Pos)
                    self.anchor3.show()

                    pt5 = QtCore.QPointF(self.pointB.x(), self.pointB.y())
                    self.line5.setLine(pt4.x(), pt4.y(), pt5.x(), pt5.y())
                    self.scene().addItem(self.line5)
                    self.flag = False
                    self.flag1 = False
                    return
                else:
                    # self.anchor1.show()
                    # self.anchor2.show()
                    # self.anchor3.show()
                    self.line1.setLine(self.pointA.x(), self.pointA.y(), self.anchor1Pos.x(), self.pointA.y())
                    self.line2.setLine(self.anchor1Pos.x(), self.pointA.y(), self.anchor1Pos.x(), self.anchor2Pos.y())
                    self.line3.setLine(self.anchor1Pos.x(), self.anchor2Pos.y(), self.anchor3Pos.x(), self.anchor2Pos.y())
                    self.line4.setLine(self.anchor3Pos.x(), self.anchor2Pos.y(), self.anchor3Pos.x(), self.pointB.y())
                    self.line5.setLine(self.anchor3Pos.x(), self.pointB.y(), self.pointB.x(), self.pointB.y())

                    self.anchor1Pos = QPointF(self.line2.line().x1(), (self.line2.line().y1()+self.line2.line().y2()/2))
                    # self.anchor1.setPos(self.anchor1Pos)
                    self.anchor1.show() 

                    self.anchor2Pos = QPointF((self.line3.line().x1()+self.line3.line().x2())/2, self.line3.line().y1())
                    # self.anchor2.setPos(self.anchor2Pos)
                    self.anchor2.show() 

                    self.anchor3Pos = QPointF(self.line4.line().x1(), (self.line4.line().y1()+self.line4.line().y2()/2))
                    # self.anchor3.setPos(self.anchor3Pos)
                    self.anchor3.show() 
                    
                    return

            else:
                self.line1.setLine(self.pointA.x(), self.pointA.y(), self.anchor1Pos.x(), self.pointA.y())
                self.line2.setLine(self.anchor1Pos.x(), self.pointA.y(), self.anchor1Pos.x(), self.pointB.y())
                self.line3.setLine(self.anchor1Pos.x(), self.pointB.y(), self.pointB.x(), self.pointB.y())
                
                self.anchor1Pos = QPointF(self.line2.line().x1(), (self.line2.line().y1()+self.line2.line().y2()/2))
                self.anchor1.show() 

                self.line4.setLine(0,0,0,0)
                self.line5.setLine(0,0,0,0)
                self.anchor2.hide()
                self.anchor3.hide()
            self.flag = False
        elif self.connection_line == 2:
            if self.pointB.x() < self.pointA.x():
                if self.flag1:
                    pt1 = QtCore.QPointF(self.pointA.x()+13, self.pointA.y())
                    self.line1.setLine(self.pointA.x(), self.pointA.y(), pt1.x(), pt1.y())
                   
                    pt2 = QtCore.QPointF(self.pointA.x()+13 , self.pointA.y()-20)
                    self.line2.setLine(pt1.x(), pt1.y(), pt2.x(), pt2.y())
                   
                    pos = QPointF(pt1.x(), (pt1.y()+pt2.y())/2) 
                    self.anchor1.set_pos(pos)
                    self.anchor1Pos = pos
                    self.anchor1.setPos(self.anchor1Pos)
                    self.anchor1.show()
                
                    pt3 = QtCore.QPointF(self.pointB.x(),  self.pointA.y()-20)
                    self.line3.setLine(pt2.x(), pt2.y(), pt3.x(), pt3.y())

                    pos = QPointF((pt2.x()+pt3.x())/2, pt2.y()) 
                    self.anchor2.set_pos(pos)
                    self.anchor2Pos = pos
                    self.anchor2.setPos(self.anchor2Pos)
                    self.anchor2.show()

                    pt4 = QtCore.QPointF(self.pointB.x(), self.pointB.y())
                    self.line4.setLine(pt3.x(), pt3.y(), pt4.x(), pt4.y())
                    self.scene().addItem(self.line4)
                
                    self.anchor3.hide()
                    self.flag = False
                    self.flag1 = False
                    return
                else:
                    self.line1.setLine(self.pointA.x(), self.pointA.y(), self.anchor1Pos.x(), self.pointA.y())
                    self.line2.setLine(self.anchor1Pos.x(), self.pointA.y(), self.anchor1Pos.x(), self.anchor2Pos.y())
                    self.line3.setLine(self.anchor1Pos.x(), self.anchor2Pos.y(), self.pointB.x(), self.anchor2Pos.y())
                    self.line4.setLine(self.pointB.x(), self.anchor2Pos.y(), self.pointB.x(), self.pointB.y())

                    self.anchor1Pos = QPointF(self.line2.line().x1(), (self.line2.line().y1()+self.line2.line().y2()/2))
                    self.anchor1.show() 

                    self.anchor2Pos = QPointF((self.line3.line().x1()+self.line3.line().x2())/2, self.line3.line().y1())
                    self.anchor2.show() 
                    return

            self.line1.setLine(self.pointA.x(), self.pointA.y(), self.pointB.x(), self.pointA.y())
            self.line2.setLine(self.pointB.x(), self.pointA.y(), self.pointB.x(), self.pointB.y())
        
            self.line3.setLine(0,0,0,0)
            self.line4.setLine(0,0,0,0)
            self.line5.setLine(0,0,0,0)
            self.anchor1.hide()
            self.anchor2.hide()
            self.anchor3.hide()
        elif self.connection_line == 3:
            if self.pointB.x() < self.pointA.x():
                if self.flag1:
                    self.line1.setLine(0, 0, 0, 0)

                    pt2 = QtCore.QPointF(self.pointA.x(), self.pointA.y()-20)
                    self.line2.setLine(self.pointA.x(), self.pointA.y(), pt2.x(), pt2.y())
                   
                    pt3 = QtCore.QPointF(self.pointB.x()-13 , self.pointA.y()-20)
                    self.line3.setLine(pt2.x(), pt2.y(), pt3.x(), pt3.y())

                    self.anchor1.hide()

                    pos = QPointF((pt2.x()+pt3.x())/2, pt2.y()) 
                    self.anchor2.set_pos(pos)
                    self.anchor2Pos = pos
                    self.anchor2.setPos(self.anchor2Pos)
                    self.anchor2.show()
                
                    pt4 = QtCore.QPointF(self.pointB.x()-13,  self.pointB.y())
                    self.line4.setLine(pt3.x(), pt3.y(), pt4.x(), pt4.y())
                    self.scene().addItem(self.line4)

                    pt5 = QtCore.QPointF(self.pointB.x(), self.pointB.y())
                    self.line5.setLine(pt4.x(), pt4.y(), pt5.x(), pt5.y())
                    self.scene().addItem(self.line5)
                
                    pos = QPointF(pt3.x(), (pt3.y()+pt4.y())/2) 
                    self.anchor3.set_pos(pos)
                    self.anchor3Pos = pos
                    self.anchor3.setPos(self.anchor3Pos)
                    self.anchor3.show()

                    self.flag = False
                    self.flag1 = False
                    return
                else:
                    self.line2.setLine(self.pointA.x(), self.pointA.y(), self.pointA.x(), self.anchor2Pos.y()) 
                    self.line3.setLine(self.pointA.x(), self.anchor2Pos.y(), self.anchor3Pos.x(), self.anchor2Pos.y())
                    self.line4.setLine(self.anchor3Pos.x(), self.anchor2Pos.y(), self.anchor3Pos.x(), self.pointB.y())
                    self.line5.setLine(self.anchor3Pos.x(), self.pointB.y(), self.pointB.x(), self.pointB.y())

                    self.anchor2Pos = QPointF((self.line3.line().x1()+self.line3.line().x2())/2, self.line3.line().y1())
                    self.anchor2.show() 

                    self.anchor3Pos = QPointF(self.line4.line().x1(), (self.line4.line().y1()+self.line4.line().y2())/2)
                    self.anchor3.show()
                    return

            self.line1.setLine(self.pointA.x(), self.pointA.y(), self.pointA.x(), self.pointB.y())
            self.line2.setLine(self.pointA.x(), self.pointB.y(), self.pointB.x(), self.pointB.y())
        
            self.line3.setLine(0,0,0,0)
            self.line4.setLine(0,0,0,0)
            self.line5.setLine(0,0,0,0)
            self.anchor1.hide()
            self.anchor2.hide()
            self.anchor3.hide()
        elif self.connection_line == 4:
            if self.pointB.x() < self.pointA.x():
                if self.flag1:
                    self.line1.setLine(0,0,0,0)

                    pt2 = QtCore.QPointF(self.pointA.x(), self.pointA.y()+20)
                    self.line2.setLine(self.pointA.x(), self.pointA.y(), pt2.x(), pt2.y())
                   
                    pt3 = QtCore.QPointF(self.pointB.x()-13 , self.pointA.y()+20)
                    self.line3.setLine(pt2.x(), pt2.y(), pt3.x(), pt3.y())
                   
                    self.anchor1.hide()
                    
                    pos = QPointF((pt2.x()+pt3.x())/2, pt3.y()) 
                    self.anchor2.set_pos(pos)
                    self.anchor2Pos = pos
                    self.anchor2.setPos(self.anchor2Pos)
                    self.anchor2.show()


                    pt4 = QtCore.QPointF(self.pointB.x()-13,  self.pointB.y())
                    self.line4.setLine(pt3.x(), pt3.y(), pt4.x(), pt4.y())
                    self.scene().addItem(self.line4)

                    pt5 = QtCore.QPointF(self.pointB.x(), self.pointB.y())
                    self.line5.setLine(pt4.x(), pt4.y(), pt5.x(), pt5.y())
                    self.scene().addItem(self.line5)
                
                    pos = QPointF(pt4.x(), (pt3.y()+pt4.y())/2) 
                    self.anchor3.set_pos(pos)
                    self.anchor3Pos = pos
                    self.anchor3.setPos(self.anchor3Pos)
                    self.anchor3.show()

                    self.flag = False
                    self.flag1 = False
                    return
                else:
                    self.line2.setLine(self.pointA.x(), self.pointA.y(), self.pointA.x(), self.anchor2Pos.y())
                    self.line3.setLine(self.pointA.x(), self.anchor2Pos.y(), self.anchor3Pos.x(), self.anchor2Pos.y())
                    self.line4.setLine(self.anchor3Pos.x(), self.anchor2Pos.y(), self.anchor3Pos.x(), self.pointB.y())
                    self.line5.setLine(self.anchor3Pos.x(), self.pointB.y(), self.pointB.x(), self.pointB.y())

                    self.anchor2Pos = QPointF((self.line3.line().x1()+self.line3.line().x2())/2, self.line3.line().y1())
                    self.anchor2.show() 

                    self.anchor3Pos = QPointF(self.line4.line().x1(), (self.line4.line().y1()+self.line4.line().y2())/2)
                    self.anchor3.show() 
                    return


            self.line1.setLine(self.pointA.x(), self.pointA.y(), self.pointA.x(), self.pointB.y())
            self.line2.setLine(self.pointA.x(), self.pointB.y(), self.pointB.x(), self.pointB.y())
        
            self.line3.setLine(0,0,0,0)
            self.line4.setLine(0,0,0,0)
            self.line5.setLine(0,0,0,0)
            self.anchor1.hide()
            self.anchor2.hide()
            self.anchor3.hide()
        elif self.connection_line == 5:

            if self.pointB.x() < self.pointA.x():
                if self.flag1:
                    pt1 = QtCore.QPointF(self.pointA.x()+13, self.pointA.y())
                    self.line1.setLine(self.pointA.x(), self.pointA.y(), pt1.x(), pt1.y())
                   
                    pt2 = QtCore.QPointF(self.pointA.x()+13 , (self.pointA.y()+self.pointB.y())/2)
                    self.line2.setLine(pt1.x(), pt1.y(), pt2.x(), pt2.y())
                   
                    pos = QPointF(pt1.x(), (pt1.y()+pt2.y())/2) 
                    self.anchor1.set_pos(pos)
                    self.anchor1Pos = pos
                    self.anchor1.setPos(self.anchor1Pos)
                    self.anchor1.show()

                    pt3 = QtCore.QPointF(self.pointB.x(),  (self.pointA.y()+self.pointB.y())/2)
                    self.line3.setLine(pt2.x(), pt2.y(), pt3.x(), pt3.y())

                    pos = QPointF((pt2.x()+pt3.x())/2, pt3.y()) 
                    self.anchor2.set_pos(pos)
                    self.anchor2Pos = pos
                    self.anchor2.setPos(self.anchor2Pos)
                    self.anchor2.show()

                    pt4 = QtCore.QPointF(self.pointB.x(), self.pointB.y())
                    self.line4.setLine(pt3.x(), pt3.y(), pt4.x(), pt4.y())
                    self.scene().addItem(self.line4)
                
                 
                    self.anchor3.hide()

                    self.flag = False
                    self.flag1 = False
                    return
                else:
                    self.line1.setLine(self.pointA.x(), self.pointA.y(), self.anchor1Pos.x(), self.pointA.y())
                    self.line2.setLine(self.anchor1Pos.x(), self.pointA.y(), self.anchor1Pos.x(), self.anchor2Pos.y())
                    self.line3.setLine(self.anchor1Pos.x(), self.anchor2Pos.y(), self.pointB.x(), self.anchor2Pos.y())
                    self.line4.setLine(self.pointB.x(), self.anchor2Pos.y(), self.pointB.x(), self.pointB.y())

                    self.anchor1Pos = QPointF(self.line2.line().x1(), (self.line2.line().y1()+self.line2.line().y2())/2)
                    self.anchor1.show() 

                    self.anchor2Pos = QPointF((self.line3.line().x1()+self.line3.line().x2())/2, self.line3.line().y1())
                    self.anchor2.show() 
                    return

            self.line1.setLine(self.pointA.x(), self.pointA.y(), self.pointB.x(), self.pointA.y())
            self.line2.setLine(self.pointB.x(), self.pointA.y(), self.pointB.x(), self.pointB.y())
        
            self.line3.setLine(0,0,0,0)
            self.line4.setLine(0,0,0,0)
            self.line5.setLine(0,0,0,0)
            self.anchor1.hide()
            self.anchor2.hide()
            self.anchor3.hide()

        elif self.connection_line == 6:
            self.line1.setLine(self.pointA.x(), self.pointA.y(), self.pointA.x(), (self.pointA.y()+self.pointB.y())/2)
            self.line2.setLine(self.pointA.x(), (self.pointA.y()+self.pointB.y())/2, self.pointB.x(), (self.pointA.y()+self.pointB.y())/2)
            self.line3.setLine(self.pointB.x(), (self.pointA.y()+self.pointB.y())/2, self.pointB.x(), self.pointB.y())
                
            # self.anchor1Pos = QPointF(self.line2.line().x1(), (self.line2.line().y1()+self.line2.line().y2()/2))
            # self.anchor1.show() 

            self.line4.setLine(0,0,0,0)
            self.line5.setLine(0,0,0,0)
            self.anchor1.hide()
            self.anchor2.hide()
            self.anchor3.hide()

    def paint(self, painter, option, widget):
        if self.isSelected():
            painter.setPen(self.selPen)
            painter.setBrush(self.brush)
            painter.drawPath(self.path())
        else:
            painter.setPen(self.pen)
            painter.setBrush(self.brush)
            painter.drawPath(self.path())

    @property
    def pointA(self):
        return self._pointA
 
    @pointA.setter
    def pointA(self, point):
        self._pointA = point
        self.init_path(self.connection_line)

    # @pointA.setter
    def pointA0(self, point, mousePos):
        self._pointA = point
        # print("in func A0")
        if self.flaggg:
            # self.anchor1Pos = QPointF((self.anchor1Pos.x()+mousePos.x())/2, (self.pointA.y()+self.pointB.y())/2)
            self.anchor2Pos = QPointF((self.anchor1Pos.x()+mousePos.x())/2, (self.pointA.y()+self.pointB.y())/2)
            self.anchor3Pos = QPointF(mousePos.x()-13, (self.anchor2Pos.y()+self.pointB.y())/2)
            self.anchor1.anchorMoveEvent()
            self.anchor2.anchorMoveEvent()
            self.anchor3.anchorMoveEvent()
            self.updatePath()
            return 
        self.anchor1.anchorMoveEvent()
        self.anchor2.anchorMoveEvent()
        self.anchor3.anchorMoveEvent()
        self.updatePath()  

    @property
    def pointB(self):
        return self._pointB
 
    @pointB.setter
    def pointB(self, point):
        self._pointB = point
        self.init_path(self.connection_line)
 
    # @pointB.setter
    def pointB0(self, point, mousePos):
        self._pointB = point
        
        if self.flaggg: 
            self.anchor2Pos = QPointF((self.anchor1Pos.x()+mousePos.x())/2, (self.pointA.y()+self.pointB.y())/2)
            self.anchor3Pos = QPointF(mousePos.x()-13, (self.anchor2Pos.y()+self.pointB.y())/2)
            self.anchor1.anchorMoveEvent()
            self.anchor2.anchorMoveEvent()
            self.anchor3.anchorMoveEvent()
            self.updatePath()
            return
        self.anchor1.anchorMoveEvent()
        self.anchor2.anchorMoveEvent()
        self.anchor3.anchorMoveEvent()
        self.updatePath()
        
    @property
    def source(self):
        return self._source
 
    @source.setter
    def source(self, widget):
        self._source = widget
 
    @property
    def target(self):
        return self._target
 
    @target.setter
    def target(self, widget):
        self._target = widget

    def __delete__(self,instance):
        del self._source
        del self._target
        del self._pointA
        del self._pointB

class NodeSocket(QtWidgets.QGraphicsItem):
    
    def __init__(self, rect, parent, type, nature):
        # type is the number of input/output
        # 1 means that this socket will save one positon (converge to or diverge from one line / pos)
        # 0 means that this socket will save multiple positons in a list (inPos, outPos lists)

        # nature is the orientation of node socket : horizontal or vertical (left/right or up/down)
        # 0 means that horizontal (left/right)
        # 1 means vertical up
        # 2 means vertical down 

        super(NodeSocket, self).__init__(parent)
        self.rect = rect
        self.typee = 'Graphics.NodeSocket'
        self.type = type
        self.nature = nature
        self.parent = parent
        self.connection = -1
        self.setAcceptHoverEvents(True)
        self.newLine=None
        self.otherLine=None
        self.setZValue(1000)
        if (parent.type == 'none'):
            self.setFlag(QGraphicsItem.ItemIsMovable)
    
        # Brush.
        self.brush = QtGui.QBrush()
        self.brush.setStyle(QtCore.Qt.SolidPattern)
        self.brush.setColor(QtGui.QColor(255,255,255,0)) #  220,220,220,220
        # Pen.
        self.pen = QtGui.QPen()
        self.pen.setStyle(QtCore.Qt.SolidLine)
        self.pen.setWidth(2)
        self.pen.setColor(QtGui.QColor(255,255,255,0)) #20,20,20,255
    
        self.selPen = QtGui.QPen()
        self.selPen.setStyle(QtCore.Qt.SolidLine)
        self.selPen.setWidth(2)
        self.selPen.setColor(QtGui.QColor(222,192,222))
               
        self.pos = QtCore.QPointF()
        self.inPos = []
        self.outPos = []
        self.inLines = []
        self.outLines = []
        
    def shape(self):
        path = QtGui.QPainterPath()
        path.addRect(self.boundingRect())
        return path
 
    def boundingRect(self):
        return QtCore.QRectF(self.rect)
 
    def paint(self, painter, option, widget):
        painter.setPen(self.pen)
        painter.drawRect(QtCore.QRectF(self.rect))

    def mousePressEvent(self, event):
        if Graphics.flag:
            cursor = QCursor( Qt.PointingHandCursor )
            QApplication.instance().setOverrideCursor(cursor)

            if self.typee == 'Graphics.NodeSocket':
                if self.type == 0:
                    rect = self.boundingRect()
                    pointA = event.scenePos()
                    pointB = self.mapToScene(event.pos())
                    self.newLine = NodeLine(pointA, pointB)
                    self.outLines.append(self.newLine)
                    self.outPos.append(self.mapFromScene(pointA))
                    self.scene().addItem(self.newLine)    
                    self.newLine.pointA = self.mapToScene(self.getCenter(len(self.outLines)-1,0))  
                elif self.type == 1:
                    rect = self.boundingRect()
                    pointA = event.scenePos()
                    pointB = self.mapToScene(event.pos())
                    self.newLine = NodeLine(pointA, pointB)
                    self.outLines.append(self.newLine)
                    self.pos = self.mapFromScene(pointA)
                    self.scene().addItem(self.newLine)    
                    self.newLine.pointA = self.mapToScene(self.getCenter(0, 0))  
            else:
                super(NodeSocket, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        try:
            pointB = self.mapToScene(event.pos())
            self.newLine.pointB = pointB
            if self.otherLine:
                self.otherLine.pointB=pointB
        except Exception as e:
            print(e)
        super(NodeSocket, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        item = self.scene().itemAt(event.scenePos().toPoint(),QtGui.QTransform())
        if not item == None:
            item.otherLine=self.newLine
        print(type(item), item)
        if not item == None:
            if self.typee == item.typee:
                if item.type == 0:
                    self.newLine.source = self
                    self.newLine.target = item
                    self.newLine.pointB =  event.scenePos()
                    item.inLines.append(self.newLine)
                    item.inPos.append(item.mapFromScene(self.newLine.pointB))
                    self.newLine.pointB = item.mapToScene(item.getCenter(len(self.inLines)-1,1))
                elif item.type == 1:
                    self.newLine.source = self
                    self.newLine.target = item
                    self.newLine.pointB =  event.scenePos()
                    item.inLines.append(self.newLine)
                    item.pos = item.mapFromScene(self.newLine.pointB)
                    self.newLine.pointB = item.mapToScene(item.getCenter(0, 1))

                if self.nature == 0 and item.nature == 0: 
                    self.newLine.connection_line = 1
                    self.newLine.init_path(1)
                    # item.parent.connection_line = 1
                elif self.nature == 0 and item.nature == 1: 
                    self.newLine.connection_line = 2
                    self.newLine.init_path(2)
                elif self.nature == 1 and item.nature == 0:
                    self.newLine.connection_line = 3
                    self.newLine.init_path(3)
                elif self.nature == 2 and item.nature == 0:
                    self.newLine.connection_line = 4
                    self.newLine.init_path(4)
                elif self.nature == 0 and item.nature == 2:
                    self.newLine.connection_line = 5
                    self.newLine.init_path(5)
                elif self.nature == 1 and item.nature == 2:
                    self.newLine.connection_line = 6
                    self.newLine.init_path(6)
                print("connection ", self.newLine.connection_line)
        else:
            print("before removing")
            self.scene().removeItem(self.newLine.line1)
            self.scene().removeItem(self.newLine.line2)
            self.scene().removeItem(self.newLine.line3)
            self.scene().removeItem(self.newLine.line4)
            self.scene().removeItem(self.newLine.line5)
            self.scene().removeItem(self.newLine.anchor1)
            self.scene().removeItem(self.newLine.anchor2)
            self.scene().removeItem(self.newLine.anchor3)

            print("after removing")
            
            del self.newLine
            super(NodeSocket, self).mouseReleaseEvent(event) 

    def hoverEnterEvent(self, event):
        if Graphics.flag:
            cursor = QCursor( Qt.CrossCursor )
            QApplication.instance().setOverrideCursor(cursor)
        
    def hoverLeaveEvent(self, event):
        if Graphics.flag:
            cursor = QCursor( Qt.ArrowCursor )
            QApplication.instance().setOverrideCursor(cursor)

    def getCenter(self, index, io):
        rect = self.boundingRect()
        if self.type == 0:    
            if io == 1:
                center =  QtCore.QPointF(self.inPos[index])
            elif io == 0:
                center = QtCore.QPointF(self.outPos[index])
            new = QtCore.QPointF(rect.width()/2+rect.x(), center.y())
            return new
        elif self.type == 1:
            center = QtCore.QPointF(rect.x() + rect.width()/2, rect.y() + rect.height()/2)
            return center


d = {
    "Bag"                   : [[21, -4, 10, 10, 1, 1], [-4, 35, 10, 57, 0, 0], [46, 35, 10, 57, 0, 0], [0, 94, 52, 10, 0, 2]],
    "Boiler"                : [[37, -4, 10, 10, 1, 1], [-4, 35, 10, 57, 0, 0], [77, 35, 10, 57, 0, 0], [0, 95, 82, 10, 0, 2]],
    "Tank"                  : [[45, -4, 10, 10, 1, 1], [-4, 35, 10, 57, 0, 0], [94, 35, 10, 57, 0, 0], [0, 95, 100, 10, 0, 2]],
    "Centrifugal"           : [[45, -4, 10, 10, 1, 1], [4, 52, 10, 10, 1, 0], [4, 18, 10, 10, 1, 0], [45, 90, 10, 10, 1, 2], [77, 46, 10, 10, 1, 0], [94, -4, 10, 10, 1, 0]],
    "CentrifugalPump"       : [[50, 3, 10, 10, 1, 1], [-4, 43, 10, 10, 1, 0], [50, 83, 10, 10, 1, 2], [93, 43, 10, 10, 1, 0]],
    "CentrifugalPump2"      : [[45, -4, 10, 10, 1, 1], [4, 52, 10, 10, 1, 0], [4, 18, 10, 10, 1, 0], [45, 90, 10, 10, 1, 2], [77, 46, 10, 10, 1, 0], [94, -4, 10, 10, 1, 0]],
    "CentrifugalPump3"      : [[15, -4, 10, 10, 1, 1], [45, 10, 10, 10, 1, 0], [-1, 46, 10, 10, 1, 0], [35, 94, 10, 10, 1, 2], [75, 46, 10, 10, 1, 0]],
    "Column"                : [[25, -4, 10, 10, 1, 1], [-4, 15, 10, 70, 0, 0], [52, 15, 10, 70, 0, 0], [25, 94, 10, 10, 1, 2]],
    "Compressor"            : [[-3, 44, 10, 10, 1, 0], [43, -4, 10, 10, 1, 1], [85, 44, 10, 10, 1, 0], [43, 94, 10, 10, 1, 2]],
    "Cooler"                : [[12, 13, 10, 10, 1, 0], [12, 76, 10, 10, 1, 0], [85, 21, 10, 10, 1, 0], [85, 69, 10, 10, 1, 0]],
    "GasBottle"             : [[20, -4, 10, 10, 1, 1], [-4, 45, 10, 47, 0, 0], [44, 45, 10, 47, 0, 0], [0, 95, 49, 10, 0, 2]],
    "Heater"                : [[6, 44, 10, 10, 1, 0], [33, 17, 10, 10, 1, 1], [60, 44, 10, 10, 1, 0], [33, 71, 10, 10, 1, 2]],
    "HeatExchanger"         : [[-4, 44, 10, 10, 1, 0], [43, -4, 10, 10, 1, 1], [43, 94, 10, 10, 1, 2], [94, 20, 10, 10, 1, 0], [94, 69, 10, 10, 1, 0]],
    "HeatExchanger2"        : [[-4, 44, 10, 10, 1, 0], [43, -4, 10, 10, 1, 1], [94, 44, 10, 10, 1, 0], [43, 94, 10, 10, 1, 2]],
    "HorizontalVessel"      : [[8, -4, 85, 10, 0, 1], [-4, 25, 10, 10, 1, 0], [94, 25, 10, 10, 1, 0], [8, 45, 85, 10, 0, 2]],
    "LiquidRingCompressor"  : [[-5, 44, 15, 15, 1, 0], [43, -4, 15, 15, 1, 1], [90, 44, 15, 15, 1, 0], [43, 90, 15, 15, 1, 2]],
    "VerticalVessel"        : [[-4, 5, 10, 90, 0, 0], [22, -4, 10, 10, 1, 1], [45, 5, 10, 90, 0, 0], [22, 95, 10, 10, 1, 2]]
    }


class NodeItem(QtWidgets.QGraphicsItem):

    def __init__(self,unitOpType, graphicsView):
        super(NodeItem, self).__init__()

        self.name = None
        self.type = unitOpType
        self.typee = 'Graphics.NodeItem'
        # self.connection_line = -1                       # 1 = -|_  //  2 = -| // 3 = |- //  4 = _|  //  5 = |_  //  6 = |-|
        
        self.graphicsView = graphicsView    
        # self.pos = QPointF()            
        
        # if self.type == 'Cooler':
        #     self.icon = QIcon("svg/Cooler.svg")
        # elif self.type == 'Heater':
        #     self.icon = QIcon('svg/Heater.svg')
        # else:
        #     self.icon = QIcon('svg/Column.svg')

        # self.rect = QtCore.QRect(0,0,100,100)

        self.Sockets = []
        self.pic = QIcon("svg/" + self.type + ".svg").pixmap(QSize(100, 100))
        self.rect = self.pic.rect()

        list = d[self.type]
        for i in list:
            self.Sockets.append(NodeSocket(QtCore.QRectF(i[0], i[1], i[2], i[3]), self, i[4], i[5]))

        self.text = QGraphicsTextItem(self)
        f = QFont()
        f.setPointSize(8)
        self.text.setFont(f)
        self.text.setDefaultTextColor(QtGui.QColor(73,36,73,255))
        self.text.setParentItem(self)
        self.text.setPos(self.rect.width()-(self.rect.width()*0.85), self.rect.height())
        self.text.setPlainText(self.name) 
        
        self.setAcceptHoverEvents(True)
        self.setFlag(QtWidgets.QGraphicsPixmapItem.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsPixmapItem.ItemIsSelectable)
        # self.Sockets = [NodeSocket(QtCore.QRect(-4, 15, 10, 70), self, 0, 0),
        #                 NodeSocket(QtCore.QRect(93, 20, 10, 10), self, 1, 0), 
        #                 NodeSocket(QtCore.QRect(93, 60, 10, 10), self, 1, 0),]

        # Brush
        self.brush = QtGui.QBrush()
        self.brush.setStyle(QtCore.Qt.SolidPattern)
        self.brush.setColor(QtGui.QColor(80,0,90,255))

        # Pen.
        self.pen = QtGui.QPen()
        self.pen.setStyle(QtCore.Qt.SolidLine)
        self.pen.setWidth(2)
        self.pen.setColor(QtGui.QColor(20,20,20,255))
    
        self.selPen = QtGui.QPen()
        self.selPen.setStyle(QtCore.Qt.SolidLine)
        self.selPen.setWidth(2)
        self.selPen.setColor(QtGui.QColor(222,192,222))
        lst.append(self)

    def shape(self):
        path = QtGui.QPainterPath()
        path.addRect(self.boundingRect())
        return path
 
    def boundingRect(self):
        return QtCore.QRectF(self.rect)
 
    def paint(self, painter, option, widget):
        # painter.drawPixmap(self.rect, self.icon.pixmap(QSize(1000, 1000)))
        painter.drawPixmap(self.rect, self.pic)


    def mouseMoveEvent(self, event):
        super(NodeItem, self).mouseMoveEvent(event)
        try: 
            # self.pos = event.scenePos()
            pos = self.pos()
            for socket in self.Sockets:
                for index, line in enumerate(socket.outLines):
                    # if self.connection_line == 0:
                    # line.pointA0 = (self.mapToScene(line.source.getCenter(index, 0)))
                    line.pointA0(self.mapToScene(line.source.getCenter(index, 0)), pos)
                    
                    # if line.pointB.x() - line.pointA.x() > 30:
                    #     line.init_path(line.connection_line)
                for index, line in enumerate(socket.inLines):
                    # if self.connection_line == 1:
                    # line.pointB0 = (self.mapToScene(line.target.getCenter(index, 1)))
                    line.pointB0(self.mapToScene(line.target.getCenter(index, 1)), pos)
                    # if line.pointB.x() - line.pointA.x() > 30:
                    #     line.init_path(line.connection_line)
            
        except Exception as e:
            print(e)
    
    def mouseReleaseEvent(self, event):
        super(NodeItem, self).mouseReleaseEvent(event)
        try: 
            for socket in self.Sockets:
                socket.pen.setColor(QtGui.QColor(255,255,255,0))
                socket.paint
        except Exception as e:
            print(e)

    def mouseDoubleClickEvent(self, event):
        pass

    def hoverEnterEvent(self, event):
        for socket in self.Sockets:
            socket.pen.setColor(QtGui.QColor(222,192,222))
            socket.paint

    def hoverLeaveEvent(self, event):
        for socket in self.Sockets:
            socket.pen.setColor(QtGui.QColor(255,255,255,0))
            socket.paint
