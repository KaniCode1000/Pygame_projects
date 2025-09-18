# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 18:16:08 2021

@author: Coderkani
"""
import pygame
import math

class Node:
    def __init__(self, coordinates):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.z = coordinates[2]
        
class Edge:
    def __init__(self, start, stop):
        self.start = start
        self.stop  = stop
class Wireframe:
    def __init__(self):
        self.nodes = []
        self.edges = []
    def addNodes(self, nodeList):
        for node in nodeList:
            self.nodes.append(Node(node))
    def addEdges(self, edgeList):
        for (start, stop) in edgeList:
            self.edges.append(Edge(self.nodes[start], self.nodes[stop]))
    def outputNodes(self):
        print("\n --- Nodes --- ")
        for i, node in enumerate(self.nodes):
            print(" %d: (%.2f, %.2f, %.2f)" % (i, node.x, node.y, node.z))
                
    def outputEdges(self):
        print("\n --- Edges --- ")
        for i, edge in enumerate(self.edges):
            print(" %d: (%.2f, %.2f, %.2f)" % (i, edge.start.x, edge.start.y, edge.start.z))
            print("to (%.2f, %.2f, %.2f)" % (edge.stop.x,  edge.stop.y,  edge.stop.z))
    def translate(self, axis, d):
        """ Translate each node of a wireframe by d along a given axis. """
            
        if axis in ['x', 'y', 'z']:
            for node in self.nodes:
                setattr(node, axis, getattr(node, axis) + d)
    def scale(self, centre_x, centre_y, scale):
        """ Scale the wireframe from the centre of the screen. """
        for node in self.nodes:
            node.x = centre_x + scale * (node.x - centre_x)
            node.y = centre_y + scale * (node.y - centre_y)
            node.z *= scale
    def findCentre(self):
        """ Find the centre of the wireframe. """
        num_nodes = len(self.nodes)
        meanX = sum([node.x for node in self.nodes]) / num_nodes
        meanY = sum([node.y for node in self.nodes]) / num_nodes
        meanZ = sum([node.z for node in self.nodes]) / num_nodes
        return (meanX, meanY, meanZ)
    
    
    def rotateZ(self, cx,cy,cz, radians):        
        for node in self.nodes:
            x      = node.x - cx
            y      = node.y - cy
            d      = math.hypot(y, x)
            theta  = math.atan2(y, x) + radians
            node.x = cx + d * math.cos(theta)
            node.y = cy + d * math.sin(theta)
    def rotateX(self, cx,cy,cz, radians):
        for node in self.nodes:
            y      = node.y - cy
            z      = node.z - cz
            d      = math.hypot(y, z)
            theta  = math.atan2(y, z) + radians
            node.z = cz + d * math.cos(theta)
            node.y = cy + d * math.sin(theta)
    def rotateY(self, cx,cy,cz, radians):
        for node in self.nodes:
            x      = node.x - cx
            z      = node.z - cz
            d      = math.hypot(x, z)
            theta  = math.atan2(x, z) + radians
            node.z = cz + d * math.cos(theta)
            node.x = cx + d * math.sin(theta)
    
class ProjectionViewer:
    """ Displays 3D objects on a Pygame screen """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('3d object rendering by coderkani')
        self.background = (10,10,50)
        self.wireframes = {}
        self.displayNodes = True
        self.displayEdges = True
        self.nodeColour = (255,255,255)
        self.edgeColour = (200,200,200)
        self.nodeRadius = 4       
    def rotateAll(self, axis, theta):
        """ Rotate all wireframe about their centre, along a given axis by a given angle. """
        rotateFunction = 'rotate' + axis
        for wireframe in self.wireframes.values():
            centre = wireframe.findCentre()
            getattr(wireframe, rotateFunction)(centre[0],centre[1],centre[2], theta)
            
    def run(self):
        """ Create a pygame screen until it is closed. """
        key_to_function = {
        pygame.K_LEFT:   (lambda x: x.translateAll('x', -10)),
        pygame.K_RIGHT:  (lambda x: x.translateAll('x',  10)),
        pygame.K_DOWN:   (lambda x: x.translateAll('y',  10)),
        pygame.K_UP:     (lambda x: x.translateAll('y', -10)),
        pygame.K_EQUALS: (lambda x: x.scaleAll(1.25)),
        pygame.K_MINUS:  (lambda x: x.scaleAll( 0.8)),
        pygame.K_q: (lambda x: x.rotateAll('X',  0.1)),
        pygame.K_w: (lambda x: x.rotateAll('X', -0.1)),
        pygame.K_a: (lambda x: x.rotateAll('Y',  0.1)),
        pygame.K_s: (lambda x: x.rotateAll('Y', -0.1)),
        pygame.K_z: (lambda x: x.rotateAll('Z',  0.1)),
        pygame.K_x: (lambda x: x.rotateAll('Z', -0.1))}
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.display.quit()
                    pygame.quit()
                
                elif event.type == pygame.KEYDOWN:
                    if event.key in key_to_function:
                        key_to_function[event.key](self)
                    
            self.display()
            pygame.display.flip()
        
    def addWireframe(self, name, wireframe):
        """ Add a named wireframe object. """
        self.wireframes[name] = wireframe 
    def display(self):
        """ Draw the wireframes on the screen. """
        self.screen.fill(self.background)
        for wireframe in self.wireframes.values():
            if self.displayEdges:
                for edge in wireframe.edges:
                    pygame.draw.aaline(self.screen, self.edgeColour, (edge.start.x, edge.start.y), (edge.stop.x, edge.stop.y), 1)
            if self.displayNodes:
                for node in wireframe.nodes:
                    pygame.draw.circle(self.screen, self.nodeColour, (int(node.x), int(node.y)), self.nodeRadius, 0)
    def translateAll(self, axis, d):
        """ Translate all wireframes along a given axis by d units. """
        for wireframe in self.wireframes.values():
            wireframe.translate(axis,d)
    def scaleAll(self, scale1):
        """ Scale all wireframes by a given scale, centred on the centre of the screen. """
        centre_x = self.width/2
        centre_y = self.height/2
        for wireframe in self.wireframes.values():
            wireframe.scale(centre_x, centre_y, scale1)   
        
if __name__ == "__main__":
    cube = Wireframe()
    cube.addNodes([(x ,y, z) for x in (50, 250) for y in (50, 250) for z in (50, 250)])
    cube.addEdges([(n,n+4) for n in range(0,4)]+[(n,n+1) for n in range(0,8,2)]+[(n,n+2) for n in (0,1,4,5)])
    # cube.translate('x', 100)
    # cube.translate('y', -40)
    cube.rotateZ(cube.findCentre()[0],cube.findCentre()[1],cube.findCentre()[2], 0.1)
    cube.scale(200, 150, 0.75)
    pv = ProjectionViewer(400, 300)
    pv.addWireframe('cube', cube)
    pv.run()
    
    
    
    
    
    
    