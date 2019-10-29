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

def place_blks(block_name, block_height, block_angles, block_width, block_positions):
    try: block_positions.shape[1]
    except IndexError:
        block_positions = num.array([block_positions,
                                       num.zeros(shape=block_positions.shape)])
    with nd.Cell(block_name) as blk_arr:
        for w in num.arange(block_angles.size):
            block_pts = geom.parallelogram(length=block_width[w],
                                           height=block_height,
                                           angle=block_angles[w],
                                           shift=(block_positions[0,w],
                                                  block_positions[1,0], 0))
            nd.Polygon(points=block_pts, layer='layer3').put(0)
    blk_arr.put(0)
    message = 'Angle = '+num.array2string(blk_angles[0])+\
              ' to '+num.array2string(block_angles[-1])+\
    ', width = ' + num.array2string(block_width[0]*num.sin(num.pi/180*block_angles[0]))
    nd.text(text=message, height=20, layer=3).put(2*block_positions[0,-1] -
                                                    block_positions[0,-2],
                                                    block_positions[1,-1])

if __name__ == "__main__":

    blk_height = 20
    blk_angles = 10 * (2.0 + num.arange(7))
    blk_width = 5.0 * num.ones(blk_angles.size) / num.sin(num.pi / 180 * blk_angles)
    blk_x_positions = 80.0 * (1 + num.arange(blk_angles.size)) # x-positions
    blk_y_positions = 40.0 * num.arange(5) - 20
    blk_name = num.array2string(1+num.arange(blk_y_positions.size))
    place_cross(0, 0, 3, 60) # x, y, cross_width, cross_length
    place_cross(0, 80, 5, 60)
    place_cross(0, 160, 10, 60)
    nd.text(text='Height = 60, Width = 3',height=20,layer='layer3').put(-300,0)
    nd.text(text='Height = 60, Width = 5',height=20,layer='layer3').put(-300,80)
    nd.text(text='Height = 60, Width = 10',height=20,layer='layer3').put(-300,160)

    for i in range(5):
        place_blks(blk_name[i], blk_height, blk_angles, blk_width
                   +2.0*i*num.ones(blk_angles.size) / num.sin(num.pi / 180 * blk_angles),
                   num.array([blk_x_positions,
                              blk_y_positions[i]
                              * num.ones(shape=blk_x_positions.shape)]))

    nd.export_gds(filename='ms_test_struct_v2')
