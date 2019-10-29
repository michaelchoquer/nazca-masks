import nazca as nd
import nazca.geometries as geom
import numpy as num

nd.add_layer(name='layer3', layer=3, accuracy=.001)


# Build cross structures (this took way too long)

def place_cross(x, y, cross_w, cross_l):
    with nd.Cell(name='cross') as xs:
        xs_box_v = geom.transform(points=geom.box(length=cross_l, width=cross_w),
                                  move=(+x - cross_l / 2, y, 0))
        xs_box_h = geom.transform(points=geom.box(length=cross_w, width=cross_l),
                                  move=(+x - cross_w / 2, y, 0))
        xs_box_30 = geom.transform(geom.parallelogram(length=2 * cross_w,
                                                      height=cross_l / 2,
                                                      angle=30),
                                   move=(+x - num.sqrt(3) * cross_l / 4 - cross_w,
                                         +y - cross_l / 4, 0))
        xs_box_60 = geom.transform(geom.parallelogram(
            length=cross_w / num.sqrt(3) * 2, height=cross_l,
            angle=60),
            move=(+x - cross_l / (2 * num.sqrt(3))
                  - cross_w / num.sqrt(3),
                  +y - cross_l / 2, 0))
        xs_box_120 = geom.transform(xs_box_60, flipy=True, move=(0, +2 * y, 0))
        xs_box_150 = geom.transform(xs_box_30, flipx=True, move=(+2 * x, 0, 0))
        nd.Polygon(points=xs_box_v, layer='layer3').put(0)
        nd.Polygon(points=xs_box_h, layer='layer3').put(0)
        nd.Polygon(points=xs_box_30, layer='layer3').put(0)
        nd.Polygon(points=xs_box_60, layer='layer3').put(0)
        nd.Polygon(points=xs_box_120, layer='layer3').put(0)
        nd.Polygon(points=xs_box_150, layer='layer3').put(0)
    xs.put(0)
    return


if __name__ == "__main__":

    place_cross(0, 0, 5, 40)

    blk_height = 20
    blk_angles = 10 * (2.0 + num.arange(7))
    blk_width = 5.0 * num.ones(blk_angles.size) / num.sin(num.pi / 180 * blk_angles)
    blk_positions = 80.0 * (1 + num.arange(blk_angles.size))
    with nd.Cell(name='blocks') as blks:
        for w in num.arange(blk_angles.size):
            blk_pts = geom.parallelogram(length=blk_width[w], height=blk_height,
                                         angle=blk_angles[w],
                                         shift=(blk_positions[w], 0, 0))
            print(blk_pts)
            nd.Polygon(points=blk_pts, layer='layer3').put(0)
    blks.put(0)

    nd.export_gds(filename='ms_test_struct_v2')
