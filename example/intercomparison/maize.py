"""Script for generating intercomparison results for a maize canopy"""


from alinea.caribu.data_samples import maize_pgl_scene
from alinea.caribu.CaribuScene import CaribuScene
from alinea.astk.sun_and_sky import sky_sources
from alinea.caribu.light import light_sources


scene, mapping = maize_pgl_scene()
sources = sky_sources()
light = light_sources(*sources)
cs = CaribuScene(scene, light=light)