from pathlib import Path
from PIL import Image

SPRITE_WIDTH = 296
SPRITE_HEIGHT = 320

FRAMES = 8

SS_WIDTH = SPRITE_WIDTH * FRAMES
SS_HEIGHT = SPRITE_HEIGHT

FOLDER = Path('deeper/resources/tiles/FireTorch')
NAME = 'FireTorch'

def main():
    canvas = Image.new('RGBA', (SS_WIDTH, SS_HEIGHT), (255, 0, 0, 0))

    for i in range(0, FRAMES):
        filename = FOLDER / f"{NAME}{i+1:04d}.png"
        print(filename)
        im = Image.open(filename)
        offset = (i*SPRITE_WIDTH, 0)
        canvas.paste(im, offset)
    
    #canvas.show()
    canvas.save(FOLDER / f"{NAME}Frames.png")

if __name__ == "__main__":
    main()
