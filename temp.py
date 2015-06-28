from PIL import ImageGrab
im = ImageGrab.grab()
addr = '/Users/gzxultra/IM_programming'
im.save(addr,'jpeg')
