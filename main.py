from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import DirectionalLight, CardMaker, Texture, CollisionNode, CollisionHandlerQueue, GeomNode, \
    CollisionRay, CollisionTraverser

class MyApp(ShowBase):
    def __init__(self):
        # Call the superclass constructor
        ShowBase.__init__(self)

        # This disables Panda3D's built-in camera control
        base.disableMouse()

        # Load the panda model
        self.panda = self.loader.loadModel("models/panda.egg")
        self.panda.reparentTo(self.render)
        self.panda.setPos(0, 0, -7)
        self.panda.setScale(.5, .5, .5)
        self.panda.setHpr(0, -20, 0)
        self.panda.setTag('selectable', '')

        # Set up background with an image
        cm = CardMaker('background')
        cm.setFrame(-20, 20, -15, 15)
        self.background = self.render.attachNewNode(cm.generate())
        self.background.setPos(0, 10, -5)
        self.background.setBillboardAxis()  # Make it face the camera
        # Disable the card from click detection
        self.background.node().setIntoCollideMask(0)

        # Load and apply the texture
        background_texture = self.loader.loadTexture("models/plane.jpg")
        self.background.setTexture(background_texture)

        # Initial camera setup
        self.camera.setPos(0, -20, 0)
        self.camera.lookAt(0,0,0)
        self.accept("mouse1", self.on_mouse_click)
        # Set up a directional light
        self.directional_light = DirectionalLight('directional_light')
        self.directional_light_np = self.render.attachNewNode(self.directional_light)
        self.directional_light_np.setHpr(45, -45, 0)  # Set the light direction
        self.render.setLight(self.directional_light_np)

        # Add the task for rotating the panda
        pickerNode = CollisionNode('mouseRay')
        pickerNP = self.camera.attachNewNode(pickerNode)
        pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
        self.pickerRay = CollisionRay()
        pickerNode.addSolid(self.pickerRay)
        pickerNP.show()
        self.rayQueue = CollisionHandlerQueue()
        self.cTrav = CollisionTraverser()
        self.cTrav.addCollider(pickerNP, self.rayQueue)
        self.colorSwitched = 0
        self.taskMgr.add(self.rotate_panda, 'rotate_panda')

    def rotate_panda(self, task):
        # Rotating the panda
        self.panda.setHpr(self.panda.getHpr()[0] + .1, self.panda.getHpr()[1] + 0, self.panda.getHpr()[2] + 0)
        return Task.cont

    def get_nearest_object(self):
        mouse_pos = base.mouseWatcherNode.getMouse()
        self.pickerRay.setFromLens(self.camNode, mouse_pos.getX(),mouse_pos.getY())
        self.cTrav.traverse(self.render)
        print(self.rayQueue.getNumEntries())
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            entry = self.rayQueue.getEntry(0)
            pickedNP = entry.getIntoNodePath()
            pickedNP = pickedNP.findNetTag('selectable')
            if not pickedNP.isEmpty():
                return pickedNP

        return None

    def on_mouse_click(self):
        # Check for the nearest object under the mouse
        pickedNP = self.get_nearest_object()
        if pickedNP:
            if self.colorSwitched == 0:
                self.panda.setColor(2,2,0,.5)
                self.colorSwitched = 1
            else:
                self.panda.setColor(7,0,3,1)
                self.colorSwitched = 0


app = MyApp()
app.run()
