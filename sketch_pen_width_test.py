import vsketch
import numpy as np
import vpype as vp


class PenWidthTestSketch(vsketch.SketchClass):
    # Sketch parameters:
    debug = vsketch.Param(False)
    width = vsketch.Param(5., decimals=2, unit="in")
    height = vsketch.Param(3., decimals=2, unit="in")
    min_pen_width = vsketch.Param(0.2, decimals=3, unit="mm")
    max_pen_width = vsketch.Param(1.0, decimals=3, unit="mm")
    num_steps = vsketch.Param(5)
    radius = vsketch.Param(0.5, decimals=3,unit="in")
    buffer = vsketch.Param(0.1, decimals=4,unit="in")

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size(f"{self.height}x{self.width}", landscape=True, center=False)

        y = self.radius + self.buffer
        x = self.radius + self.buffer
        for pen_width in np.linspace(self.min_pen_width, self.max_pen_width, num=self.num_steps, endpoint=True):
            vsk.penWidth(pen_width)
            vsk.fill(1)
            vsk.stroke(2)
            vsk.circle(x,y,radius=self.radius)
            pen_width_in_mm = round(pen_width / vp.convert_length("mm"),3)
            vsk.stroke(3)
            vsk.text(f"{pen_width_in_mm}mm",x=x, y=y-self.radius-self.buffer/2, align="center",size=self.buffer-5)
            x += self.radius*2 + self.buffer
            if x + self.radius > self.width:
                x = self.radius + self.buffer
                y += self.radius*2 + 2 * self.buffer
        # implement your sketch here
        # layer = layers[math.floor(vsk.random(0, len(layers)))]
        # vsk.stroke(layer)
        # vsk.circle(0, 0, self.radius, mode="radius")

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    PenWidthTestSketch.display()
