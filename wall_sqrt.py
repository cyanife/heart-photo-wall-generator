import os
from typing import List
import numpy as np

from PIL import Image


class HeartPhotoWall:
    def __init__(
        self, tile_path: str, width_aspect: int, height_aspect: int, scale: int
    ):
        self.path: str = tile_path
        self.width_aspect: int = width_aspect
        self.height_aspect: int = height_aspect
        self.scale: int = scale

    @classmethod
    def in_heart_shape(cls, canvas: int, x: int, y: int) -> bool:
        y1 = 0.618 * np.abs(x) - 0.75 * np.sqrt((canvas / 2) ** 2 - x ** 2)
        y2 = 0.618 * np.abs(x) + 0.8 * np.sqrt((canvas / 2) ** 2 - x ** 2)
        if y < y1 or y > y2:
            return False
        else:
            return True

    def make_photo_wall(self, ratio, output) -> None:

        tiles: List[str] = os.listdir(self.path)
        tiles_num: int = len(tiles)

        canvas: int = ratio * self.width_aspect * self.height_aspect * self.scale

        x_node_length: int = int(self.width_aspect * self.scale)
        y_node_length: int = int(self.height_aspect * self.scale)

        x_node_num = int(canvas / x_node_length)
        y_node_num = int(canvas / y_node_length)

        # create canvas
        image: Image = Image.new("RGBA", (canvas + x_node_length, canvas))

        tile_idx: int = 0

        # init coordinate(topleft)
        x0 = int(-canvas / 2)
        y0 = int(canvas / 2)

        # node traversal
        for yi in range(y_node_num):
            y = y0 - yi * y_node_length
            for xi in range(x_node_num):
                x = x0 + xi * x_node_length
                if self.in_heart_shape(canvas, x, y):
                    img = Image.open(
                        os.path.join(self.path, tiles[tile_idx % tiles_num])
                    )
                    img = img.resize((x_node_length, y_node_length), Image.ANTIALIAS)
                    image.paste(img, (xi * x_node_length, yi * y_node_length))
                    tile_idx += 1
                    print(tile_idx)

        image.save(output)


if __name__ == "__main__":
    HeartPhotoWall("image_sqrt", 1, 1, 200).make_photo_wall(13, "heart_sqrt.png")
