# -*- python -*-
#
#       Copyright 2015 INRIA - CIRAD - INRA
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       WebSite : https://github.com/openalea-incubator/caribu
#
# ==============================================================================
""" paths to module data file
"""
from path import path
from alinea.caribu.file_adaptor import read_can
from alinea.caribu.display import generate_scene
from alinea.caribu.label import decode_label
import pandas


def data_path(filename):
    d = path(__file__).dirname().normpath()
    fn = filename
    return d / 'data' / fn


def maize_pgl_scene():
    fn = data_path('f331s1_100plantes.can')
    can = read_can(fn)
    opt, opak, plant, elt, leaf = decode_label(can.keys())
    mapping = pandas.DataFrame(
        {'pid': can.keys(), 'plant': plant, 'metamer': leaf, 'organ': elt}).loc[
              :, ('pid', 'plant', 'metamer', 'organ')]
    return generate_scene(can), mapping.sort_values(
        ['plant', 'metamer', 'organ'])
