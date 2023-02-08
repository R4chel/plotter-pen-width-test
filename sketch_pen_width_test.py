import vsketch
import numpy as np
import vpype as vp


class PenWidthTestSketch(vsketch.SketchClass):
    # Sketch parameters:
    debug = vsketch.Param(False)
    width = vsketch.Param(5., decimals=2, unit="in")
    height = vsketch.Param(3., decimals=2, unit="in")
    landscape = vsketch.Param(True)
    min_pen_width = vsketch.Param(0.2, decimals=3, unit="mm")
    max_pen_width = vsketch.Param(1.0, decimals=3, unit="mm")
    num_steps = vsketch.Param(5)
    buffer_ratio = vsketch.Param(0.1, decimals=4)
    label = vsketch.Param(False)
    label_height = vsketch.Param(12, unit="px")
    num_layers = vsketch.Param(2)
    stroke = vsketch.Param(False)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size(f"{self.height}x{self.width}",
                 landscape=self.landscape,
                 center=False)

        x_max_radius = vsk.width / (2 * self.num_steps + (self.num_steps + 1) *
                                    (1 + self.buffer_ratio))
        y_max_radius = (vsk.height -
                        (self.label_height if self.label else 0)) / (
                            2 * self.num_layers + (self.num_layers + 1) *
                            (1 + self.buffer_ratio))

        radius = min(x_max_radius, y_max_radius)
        x_buffer = (vsk.width -
                    2 * radius * self.num_steps) / (self.num_steps + 1)
        y_buffer = ((vsk.height - (self.label_height if self.label else 0)) -
                    self.num_layers * 2 * radius) / (self.num_layers + 1)
        x = radius + x_buffer

        layers = [i + 1 for i in range(self.num_layers)]
        for pen_width in np.linspace(self.min_pen_width,
                                     self.max_pen_width,
                                     num=self.num_steps,
                                     endpoint=True):
            y = y_buffer + radius
            if self.label:
                pen_width_in_mm = round(pen_width / vp.convert_length("mm"), 3)
                vsk.stroke(max(layers) + 1)
                vsk.text(f"{pen_width_in_mm}mm",
                         x=x,
                         y=(y_buffer + self.label_height) / 2,
                         align="center",
                         size=self.label_height)
                y += self.label_height
            vsk.penWidth(pen_width)

            for layer in layers:
                vsk.fill(layer)
                if self.stroke:
                    vsk.stroke(layer)
                else:
                    vsk.noStroke()
                vsk.circle(x, y, radius=radius)
                y += radius * 2 + y_buffer
            x += radius * 2 + x_buffer
        # implement your sketch here
        # layer = layers[math.floor(vsk.random(0, len(layers)))]
        # vsk.stroke(layer)
        # vsk.circle(0, 0, self.radius, mode="radius")

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    PenWidthTestSketch.display()
