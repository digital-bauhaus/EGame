from game.egame import EGame
class Fastmode:
    def __init__(self, config, optimizers, runs):
        self.config = config
        self.optimizers = optimizers
        self.global_config = self.config.global_config
        self.resolution = (self.global_config['window']['width'],
                           self.global_config['window']['height'])
        self.parent_window = self
        self.frame_dimension = (self.global_config['frame']['width'],
                                self.global_config['frame']['height'])

        
        self.fg = FrameGeometry(self.global_config['frame']['width'],
                                self.global_config['frame']['height'])
        self.msg2Statusbar = Msg2StatusBar()
        
    def run(self):
        game = EGame(self)
        game.start()
        while game.running:
            game.update()
        result = game.result
        print(result)

    def frameGeometry(self):
        return self.fg

    def stop_timer(self):
        pass

class FrameGeometry:
    def __init__(self, width, height):
        self.w = width
        self.h = height

    def width(self):
        return self.w

    def height(self):
        return self.h

class Msg2StatusBar:
    def __init__(self):
        pass
    def emit(self, string):
        pass
