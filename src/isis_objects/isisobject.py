from pandac.PandaModules import *
#from pandac.PandaModules import NodePath, Vec3
from layout_manager import *
from ..physics.panda.manager import *


class IsisObject(NodePath):
    """ IsisObject is the decorator class for all visible objects in IsisWorld, other
    than sky, house, ground and agents """

    def  __init__(self,name=1):         
        # generate a unique name for the object, warning, unique id uses GENERATORS ID
        self.name = "IsisObject/"+self.__class__.__name__+"+"+str(id(self))
        NodePath.__init__(self,self.name)
        # store pointer to IsisObject subclass
        self.setPythonTag("isisobj", self)
        # store model offsets 
        if not hasattr(self, 'offsetVec'):
            self.offsetVec = (0,0,0,0,0,0)
        if not hasattr(self, 'pickupVec'):
            self.pickupVec = (0,0,0,0,0,0)

        if not hasattr(self,'physics'):
            raise "Error: %s missing self.physics" % self.name

        superclasses =  map(lambda x: [x,hasattr(x, 'priority') and x.priority or 101], self.__class__.__bases__)
        # call __init__ on all parent classes
        print "SUPERCLASSES", superclasses
        for sc, rank in sorted(superclasses, key=lambda x: x[1]):
            if sc.__name__ != "IsisObject":
                print sc, rank, sc.__name__, sc.__name__=="src.isis_objects.isisobject.IsisObject"
                sc.__init__(self)

        # call setup() on all appropriate parent classes
        for sc, rank in sorted(superclasses, key=lambda x: x[1]):
            if hasattr(sc,'setup'):
                sc.setup(self)
        if hasattr(self,'setup'):
            self.setup()

    def getName(self):
        return self.name
        
    def getActiveModel(self):
        return self.activeModel

