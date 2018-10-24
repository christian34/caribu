from nose.tools import assert_raises

from alinea.caribu.caribu import green_leaf_PAR, radiosity, raycasting, \
    x_radiosity, x_raycasting, mixed_radiosity, x_mixed_radiosity


def test_default_light_in_raycasting():
    pts1 = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
    triangles = [pts1]
    mats = [green_leaf_PAR]

    # default light
    res = raycasting(triangles, mats)

    assert 'area' in res


def test_default_light_in_radiosity():
    pts1 = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
    pts2 = [(0, 0, 1), (1, 0, 1), (0, 1, 1)]
    triangles = [pts1, pts2]
    mats = [green_leaf_PAR] * 2

    # default light
    res = radiosity(triangles, mats)

    assert 'area' in res


def test_other_algos():
    pts1 = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
    pts2 = [(0, 0, 1), (1, 0, 1), (0, 1, 1)]
    triangles = [pts1, pts2]
    domain = (0, 0, 1, 1)
    height = 1
    mats = [green_leaf_PAR] * 2
    x_mats = {'PAR':mats, 'NIR':mats}
    sensors = [[(0, 0, 2), (1, 0, 2), (0, 1, 2)]]
    lights = [(1, (0, 0, -1))]

    res = raycasting(triangles, mats, sensors=sensors)
    assert 'sensors' in res
    assert 'meta' in res
    assert 'Ei' in res['sensors']

    res = x_raycasting(triangles, x_mats, sensors=sensors)
    assert 'PAR' in res
    assert 'NIR' in res
    assert 'sensors' in res['PAR']
    assert 'meta' in res['PAR']
    assert 'Ei' in res['PAR']['sensors']

    res = radiosity(triangles, mats, sensors=sensors)
    assert 'sensors' in res
    assert 'meta' in res
    assert 'Ei' in res['sensors']

    res = x_radiosity(triangles, x_mats, sensors=sensors)
    assert 'PAR' in res
    assert 'NIR' in res
    assert 'sensors' in res['PAR']
    assert 'meta' in res['PAR']
    assert 'Ei' in res['PAR']['sensors']

    res = mixed_radiosity(triangles, mats, lights=lights, domain=domain,
                          soil_reflectance=0.3, diameter=1, layers=2,
                          height=height)
    assert 'Eabs' in res

    res = x_mixed_radiosity(triangles, x_mats, lights=lights, domain=domain,
                            soil_reflectance={'PAR': 0.3, 'NIR': 0.1},
                            diameter=1, layers=2,
                            height=height)
    assert 'PAR' in res
    assert 'NIR' in res
    assert 'meta' in res['PAR']
    assert 'Eabs' in res['PAR']

def test_raycasting_exception():
    points = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
    triangles = [points]

    # black body
    materials = [(0,)]
    assert_raises(ValueError, lambda: raycasting(triangles, materials))
    materials = [(0.,)]
    assert_raises(ValueError, lambda: raycasting(triangles, materials))
    materials = [(0., 0)]
    assert_raises(ValueError, lambda: raycasting(triangles, materials))
    materials = [(0., 0, 0, 0.)]
    assert_raises(ValueError, lambda: raycasting(triangles, materials))

    # unmatch
    materials = [(0.1,)] * 2
    assert_raises(ValueError, lambda: raycasting(triangles, materials))


def test_radiosity_exception():
    points = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
    triangles = [points]
    materials = [green_leaf_PAR]

    # one triangle
    assert_raises(ValueError, lambda: radiosity(triangles, materials))

    pts1 = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
    pts2 = [(0, 0, 1), (1, 0, 1), (0, 1, 1)]
    triangles = [pts1, pts2]

    # black body
    materials = [(0,)] * 2
    assert_raises(ValueError, lambda: radiosity(triangles, materials))

    # unmatch triangles <-> materials
    materials = [green_leaf_PAR]
    assert_raises(ValueError, lambda: radiosity(triangles, materials))



