from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import DirectionalLight, CardMaker, Texture


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

        # Set up background with an image
        cm = CardMaker('background')
        cm.setFrame(-15, 15, -12, 10)
        self.background = self.render.attachNewNode(cm.generate())
        self.background.setPos(0, 10, -5)
        self.background.setBillboardAxis()  # Make it face the camera

        # Load and apply the texture
        background_texture = self.loader.loadTexture("models/plane.jpg")
        self.background.setTexture(background_texture)

        # Initial camera setup
        self.camera.setPos(0, -20, 10)
        self.camera.lookAt(0,0,0)

        # Add the task for rotating the panda
        self.taskMgr.add(self.rotate_panda, 'rotate_panda')

    def rotate_panda(self, task):
        # Rotating the panda
        self.panda.setHpr(self.panda.getHpr()[0] + .1, self.panda.getHpr()[1] + 0, self.panda.getHpr()[2] + 0)
        return Task.cont


app = MyApp()
app.run()
