import os
from typing import List
import numpy as np

from PIL import Image


class CrossHeartPhotoWall:
    def __init__(
        self, tile_path: str, width_aspect: int, height_aspect: int, scale: int
    ):
        self.horizontal_path: str = os.path.join(tile_path, "horizontal")
        self.vertical_path: str = os.path.join(tile_path, "vertical")
        self.width_aspect: int = width_aspect
        self.height_aspect: int = height_aspect
        self.scale: int = scale

    @classmethod
    def in_heart_shape(cls, canvas: int, x: int, y: int) -> bool:
        y1 = 0.618 * np.abs(x) - 0.7 * np.sqrt((canvas / 2) ** 2 - x ** 2)
        y2 = 0.618 * np.abs(x) + 0.7 * np.sqrt((canvas / 2) ** 2 - x ** 2)
        if y < y1 or y > y2:
            return False
        else:
            return True

    def make_photo_wall(self, ratio, output) -> None:

        horizontal_tiles: List[str] = os.listdir(self.horizontal_path)
        vertical_tiles: List[str] = os.listdir(self.vertical_path)

        tiles_num_vertical: int = len(vertical_tiles)
        tiles_num_horizontal: int = len(horizontal_tiles)

        canvas: int = (
            ratio
            * (self.width_aspect * self.height_aspect)
            * (self.width_aspect + self.height_aspect)
            * self.scale
        )

        x_node_length: int = int(self.width_aspect * self.scale)
        y_node_length: int = int(self.height_aspect * self.scale)

        x_node_num_vertical = int(canvas / x_node_length)
        x_node_num_horizontal = int(canvas / y_node_length)
        y_node_num = int(canvas / (x_node_length + y_node_length)) * 2

        # create canvas
        image: Image = Image.new("RGBA", (canvas + 150, canvas))

        tile_idx_vertical: int = 0
        tile_idx_horizontal: int = 0

        # init coordinate(topleft)
        x0 = int(-canvas / 2)
        y0 = int(canvas / 2)

        # node traversal
        for yi in range(y_node_num):
            if yi % 2 == 0:
                y = y0 - yi // 2 * (x_node_length + y_node_length)
                for xi in range(x_node_num_vertical):
                    x = x0 + x_node_length * xi
                    if self.in_heart_shape(canvas, x, y):
                        img = Image.open(
                            os.path.join(
                                self.vertical_path,
                                vertical_tiles[tile_idx_vertical % tiles_num_vertical],
                            )
                        )
                        img = img.resize(
                            (x_node_length, y_node_length), Image.ANTIALIAS
                        )
                        image.paste(img, (int(x + canvas / 2), int(canvas / 2 - y)))
                        tile_idx_vertical += 1
                        print(tile_idx_vertical)
            else:
                y = y0 - yi // 2 * (x_node_length + y_node_length) - y_node_length
                for xi in range(x_node_num_horizontal):
                    x = x0 + y_node_length * xi
                    if self.in_heart_shape(canvas, x, y):
                        img = Image.open(
                            os.path.join(
                                self.horizontal_path,
                                horizontal_tiles[
                                    tile_idx_horizontal % tiles_num_horizontal
                                ],
                            )
                        )
                        img = img.resize(
                            (y_node_length, x_node_length), Image.ANTIALIAS
                        )
                        image.paste(
                            img, (int(x + canvas / 2 - 25), int(canvas / 2 - y))
                        )
                        tile_idx_vertical += 1
                        tile_idx_horizontal += 1
                        print(tile_idx_horizontal)

        image.save(output)


if __name__ == "__main__":
    CrossHeartPhotoWall("image", 3, 4, 50).make_photo_wall(1, "heart_cross.png")
