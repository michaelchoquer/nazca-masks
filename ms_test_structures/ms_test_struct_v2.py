import nazca as nd
import nazca.geometries as geom
import numpy as num
import nazca.bb_util

nd.add_layer(name='layer3', layer=3, accuracy=.001) # resolution in microns


def rotation_mat(theta):
    (c, s) = (num.cos(theta * num.pi / 180), num.sin(theta * num.pi / 180))
    return num.array(((c, -s), (s, c)))


@nd.bb_util.hashme('cross', 'cross_w')
def place_cross(cross_name, x, y, cross_w, cross_l):
    try:
        cross_w[0]
    except TypeError:
        cross_w = num.array([cross_w])
    with nd.Cell(name=cross_name) as xs:
        for u in num.arange(num.size(cross_w)):
            box_pts = num.array([[0, 0, cross_l, cross_l],
                                 [cross_w[u], 0, 0, cross_w[u]]])
            xs_box_h = geom.transform(points=num.transpose(box_pts),
                                      move=(+x, y + (cross_l - cross_w[u]) / 2
                                            + u * (cross_l + 50), 0))
            xs_box_v = geom.transform(points=num.transpose(
                num.dot(rotation_mat(90), box_pts)),
                move=(+x + (cross_l + cross_w[u]) / 2,
                      +y + u * (cross_l + 50), 0))
            xs_box_30 = geom.transform(points=num.transpose(
                num.dot(rotation_mat(30), box_pts)),
                move=(+x + (cross_l - cross_l * num.cos(num.pi / 6)
                            + cross_w[u] * num.sin(num.pi / 6)) / 2,
                      +y + (cross_l - cross_l * num.sin(num.pi / 6)
                            - cross_w[u] * num.cos(num.pi / 6)) / 2
                      + u * (cross_l + 50), 0))
            xs_box_60 = geom.transform(points=num.transpose(
                num.dot(rotation_mat(60), box_pts)),
                move=(+x + (cross_l - cross_l * num.cos(num.pi / 3)
                            + cross_w[u] * num.sin(num.pi / 3)) / 2,
                      + y + (cross_l - cross_l * num.sin(num.pi / 3)
                             - cross_w[u] * num.cos(num.pi / 3)) / 2
                      + u * (cross_l + 50), 0))
            xs_box_120 = geom.transform(xs_box_60, flipy=True,
                                        move=(0, +2 * y + cross_l + 2*u*(cross_l + 50), 0))
            xs_box_150 = geom.transform(xs_box_30, flipx=True,
                                        move=(+2 * x + cross_l, 0, 0))
            nd.Polygon(points=xs_box_h, layer='layer3').put(0)
            nd.Polygon(points=xs_box_v, layer='layer3').put(0)
            nd.Polygon(points=xs_box_30, layer='layer3').put(0)
            nd.Polygon(points=xs_box_60, layer='layer3').put(0)
            nd.Polygon(points=xs_box_120, layer='layer3').put(0)
            nd.Polygon(points=xs_box_150, layer='layer3').put(0)
            message_txt = 'Height = ' + str(cross_l) + ', Width = ' + str(cross_w[u])
            nd.text(text=message_txt, height=20, layer='layer3') \
                .put(int(x - cross_l / 2 - 150), int(y + u * (cross_l + 50)))
    xs.put(0)
    return


@nd.bb_util.hashme('blocks', 'block_width[0]', 'block_width[-1]')
def place_blks(block_name, block_height, block_width, block_angles,
               block_x_coords, block_y_coords):
    with nd.Cell(block_name) as blk_arr:
        for u in num.arange(block_width.size):
            for v in num.arange(block_angles.size):
                block_pts = geom.parallelogram(length=block_width[u],
                                               height=block_height,
                                               angle=block_angles[v],
                                               shift=(block_x_coords[v],
                                                      block_y_coords[u], 0))
                nd.Polygon(points=block_pts, layer='layer3').put(0)
            message = 'Angle = ' + num.array2string(block_angles[0]) + \
                      ' to ' + num.array2string(block_angles[-1]) + \
                      ', Width = ' + num.array2string(block_width[0]
                                                      * num.sin(num.pi/180
                                                                *block_angles[0]))
            nd.text(text=message, height=20, layer='layer3') \
                .put(int(block_x_coords[-1] + 0.5 * block_x_coords[0]),
                     int(block_y_coords[u]))
    blk_arr.put(0)
    return blk_arr


@nd.bb_util.hashme('rects', 'rect_width[0]', 'rect_width[-1]')
def place_rects(rect_name, rect_length, rect_width, rect_angles, rect_x_coords,
                rect_y_coords):
    try:
        rect_width[0]
    except TypeError:
        rect_width = num.array([rect_width])
    with nd.Cell(rect_name) as rect_array:
        for u in num.arange(rect_y_coords.size):
            for v in num.arange(rect_angles.size):
                # (c, s) = (num.cos(rect_angles[v]*num.pi/180),
                #           num.sin(rect_angles[v]*num.pi/180))
                # rotation = num.array(((c, -s), (s, c)))
                rect_pts = num.array([[0, 0, rect_width[u], rect_width[u]],
                                      [0, rect_length, rect_length, 0]])
                rect_pts = num.transpose(num.dot(rotation_mat(rect_angles[v]), rect_pts))
                rect_pts = geom.transform(points=rect_pts, move=(rect_x_coords[v],
                                                                 rect_y_coords[u], 0))
                nd.Polygon(points=rect_pts, layer='layer3').put(0)
            message = 'Angle = ' + num.array2string(rect_angles[0]) + \
                      ' to ' + num.array2string(rect_angles[-1]) + ', width = '
            if rect_width.size == 1:
                message += rect_width
            else:
                message += num.array2string(rect_width[u])
            nd.text(text=message, height=20, layer='layer3', align='rb') \
                .put(int(rect_x_coords[-2]  + 250 ),
                     int(rect_y_coords[u]) + 100)
    rect_array.put(0)
    return rect_array


if __name__ == "__main__":
    cross_structs = place_cross('cross', -100, 0, num.array([3.0, 5.0, 10.0]), 200)

    rect_w = num.array([3, 5, 8, 10])
    rect_l = 200
    rect_a = 10 * (3.0 + num.arange(7))
    rect_x = 1.25 * rect_l * (1 + num.arange(rect_a.size))
    rect_y = 1.25 * rect_l * num.arange(rect_w.size)
    rect_structs = place_rects('rectangles', rect_l, rect_w, rect_a, rect_x, rect_y)

    with nd.Cell(name='resolution_test') as res_test_bb:
        filename_res = \
            'c:\\users\\micha\documents\\code\\nazca-mask-design\\' + \
            'ms_test_structures\\resolution_test.gds'
        res_test_bb = nd.load_gds(filename=filename_res, layermap={1: 3}, prefix='res_',
                                  newcellname='res_test')
    res_test_bb = res_test_bb.put(-325, 750)

    with nd.Cell(name='critical_dimsg') as crit_dims_bb:
        filename_crit = \
            'c:\\users\\micha\\documents\code\\nazca-mask-design' + \
            '\\ms_test_structures\\critical_dimension.gds'
        crit_dims_bb = nd.load_gds(filename=filename_crit, layermap={1: 3},
                                   newcellname='crit_dim_cell', prefix='dims_')
    dims_bb = crit_dims_bb.put((-325, 450, 0))
    nd.export_gds(filename='ms_test_struct_v2')
