# -*- coding: utf-8 -*-
"""
Example of creating a radar chart (a.k.a. a spider or star chart) [1]_.
Although this example allows a frame of either 'circle' or 'polygon', polygon
frames don't have proper gridlines (the lines are circles instead of polygons).
It's possible to get a polygon grid by setting GRIDLINE_INTERPOLATION_STEPS in
matplotlib.axis to the desired number of vertices, but the orientation of the
polygon is not aligned with the radial axes.
.. [1] http://en.wikipedia.org/wiki/Radar_chart
"""

"""
    # Modified for creating an Innovation Radar by https://gitlab.com/jag7 on 14/01/17
    http://matplotlib.org/examples/api/radar_chart.html
"""

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.spines import Spine
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection


def radar_factory(num_vars, frame='circle'):
    """Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle' | 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)
    # rotate theta such that the first axis is at the top
    theta += np.pi/2

    def draw_poly_patch(self):
        verts = unit_poly_verts(theta)
        return plt.Polygon(verts, closed=True, edgecolor='k')

    def draw_circle_patch(self):
        # unit circle centered on (0.5, 0.5)
        return plt.Circle((0.5, 0.5), 0.5)

    patch_dict = {'polygon': draw_poly_patch, 'circle': draw_circle_patch}
    if frame not in patch_dict:
        raise ValueError('unknown value for `frame`: %s' % frame)

    class RadarAxes(PolarAxes):

        name = 'radar'
        # use 1 line segment to connect specified points
        RESOLUTION = 1
        # define draw_frame method
        draw_patch = patch_dict[frame]

        def fill(self, *args, **kwargs):
            """Override fill so that line is closed by default"""
            closed = kwargs.pop('closed', True)
            return super(RadarAxes, self).fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super(RadarAxes, self).plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.concatenate((x, [x[0]]))
                y = np.concatenate((y, [y[0]]))
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            return self.draw_patch()

        def _gen_axes_spines(self):
            if frame == 'circle':
                return PolarAxes._gen_axes_spines(self)
            # The following is a hack to get the spines (i.e. the axes frame)
            # to draw correctly for a polygon frame.

            # spine_type must be 'left', 'right', 'top', 'bottom', or `circle`.
            spine_type = 'circle'
            verts = unit_poly_verts(theta)
            # close off polygon by repeating first vertex
            verts.append(verts[0])
            path = Path(verts)

            spine = Spine(self, spine_type, path)
            spine.set_transform(self.transAxes)
            return {'polar': spine}

    register_projection(RadarAxes)
    return theta

def unit_poly_verts(theta):
    """Return vertices of polygon for subplot axes.
    This polygon is circumscribed by a unit circle centered at (0.5, 0.5)
    """
    x0, y0, r = [0.5] * 3
    verts = [(r*np.cos(t) + x0, r*np.sin(t) + y0) for t in theta]
    return verts

# START

N = 12
theta = radar_factory(N, frame='circle')

# data = [
#     [u'Oferta\n(QUÉ)', 'Marca', u'Conexión', u'Presencia\n(DÓNDE)', 'Suministros', u'Organización', u'Procesos\n(CÓMO)',
#     u'Obtención de valor', 'Experiencia\nde cliente', u'Clientes\n(QUIÉN)', u'Solución', 'Plataforma'],
#     (u'Radar de la Innovación', [
#         [50, 20, 50, 60, 20, 60, 30,
#          20, 50, 70, 90, 70]]),
# ]
data = [
    ['Offering\n(WHAT)', 'Brand', 'Networking', 'Presence\n(WHERE)', 'Supply Chain', 'Organization', 'Process\n(HOW)',
    'Value Capture', 'Customer\nExperience', 'Customers\n(WHO)', 'Solution', 'Platform'],
    ('Innovation Radar', [
        [50, 20, 50, 60, 20, 60, 30,
         20, 50, 70, 90, 70]]),
]
labels = data.pop(0)

fig = plt.figure(figsize=(9, 9), facecolor='white')

area_color = '#0548ff'
for n, (title, case_data) in enumerate(data):
    ax = fig.add_subplot(1, 1, 1, projection='radar')
    # ax.xaxis.grid(True,color='gray',linestyle='-')
    # ax.yaxis.grid(True,color='gray',linestyle='-')


    ax.set_ylim(0,100) #forzar límites de 0 a 100
    ax.set_yticklabels([])
    ax.set_title(title, weight='bold', size='medium', position=(0.5, 1.1),
                 horizontalalignment='center', verticalalignment='center')
    for d in case_data:
        ax.plot(theta, d, color=area_color)
        ax.fill(theta, d, facecolor=area_color, alpha=0.5, linewidth=4)
    ax.set_varlabels(labels)
    ax.set_axis_bgcolor('#a0a1a2')

plt.show()
