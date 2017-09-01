"""Script for generating intercomparison results for a maize canopy"""

import pandas
import matplotlib.pyplot as plt
import openalea.plantgl.all as pgl

from alinea.astk.sun_and_sky import sky_sources

from alinea.caribu.CaribuScene import CaribuScene
from alinea.caribu.light import light_sources

from alinea.phenoarch.user_data import leaf_area_gompertz
from alinea.phenoarch.lightning.ratp import surfacic_point_cloud
from alinea.pyratp.interface.pgl_scene import from_scene_mesh


def get_area():
    mapping = pandas.read_csv('mapping_100_plants_ZA16_2016_05_22_red90.csv')
    gomp = leaf_area_gompertz('ZA16')
    area = gomp.loc[
           (gomp.daydate == '2016-05-22') & (gomp.plant.isin(mapping.plant)), ('plant', 'leaf_area')]
    df = mapping.loc[:,('canopy_pid', 'plant')].merge(area, how='left')
    df.leaf_area = df.leaf_area.fillna(df.leaf_area.mean())
    return dict(zip(df.canopy_pid, df.leaf_area))


def get_scene(area=None):
    scene = pgl.Scene()
    mapping = pandas.read_csv('mapping_100_plants_ZA16_2016_05_22_red90.csv')
    scene.read('100_plants_ZA16_2016_05_22_red90', 'BGEOM')
    unit = 'mm'
    if area is not None:
        spc = surfacic_point_cloud(scene, fitted_area=area, scene_unit='mm')
        scene = from_scene_mesh(spc.as_scene_mesh())
        unit = 'm'
    sources = sky_sources()
    return scene, unit, mapping, sources


def run(scene, unit,  mapping, sources):
    light = light_sources(*sources)
    cs = CaribuScene(scene, light=light, scene_unit=unit)
    raw, agg = cs.run(direct=True, simplify=True)
    res = pandas.DataFrame(agg)
    res['canopy_pid'] = res.index
    res = res.merge(mapping)
    return res


def canopy_vs_mesh():
    """Compare raw mesh simulation with area-adjusted surfacic point cloud"""

    mesh = pandas.read_csv('ZA16_caribu.csv')
    can = pandas.read_csv('ZA16_area_fitted_caribu.csv')
    plt.plot(mesh['Ei'] * mesh['area'], can['Ei'] * can['area'], 'ro')
    plt.xlim(0, 0.2)
    plt.ylim(0, 0.2)
    plt.plot([0,1],[0,1],'k-')
    plt.show()