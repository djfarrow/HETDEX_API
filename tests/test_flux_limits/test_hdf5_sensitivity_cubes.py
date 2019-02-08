"""

Tests for converting between HDF5
and FITs sensitivity cubes

AUTHOR: Daniel Farrow

"""

import pytest
from hetdex_api.flux_limits.hdf5_sensitivity_cubes import SensitivityCubeHDF5Container 
from hetdex_api.flux_limits.sensitivity_cube import SensitivityCube

@pytest.fixture(scope="function")
def hdf5_container(tmpdir):
    """ HDF5 we can write test data to """
    filename = tmpdir.join("test.h5").strpath
    hdcon = SensitivityCubeHDF5Container(filename, mode="w")

    # Clever trick to close the file when we're done with it 
    yield hdcon
    hdcon.close()
    
@pytest.fixture(scope="module")
def sensitivity_cube(datadir):
    """ A sensitivity cube to add or read"""
    filename = datadir.join("test_sensitivity_cube.fits").strpath
    wavelengths = [3500.0, 5500.0]
    alphas = [-3.5, -3.5]

    return SensitivityCube.from_file(filename, wavelengths, alphas)

@pytest.mark.parametrize("use_with", [True, False])
def test_hdf5_create_and_write(tmpdir, use_with):
    """
    Test writing the HDF5 file to a 
    file
    """

    filename = tmpdir.join("test.h5").strpath

    # Test with statement
    if use_with:
        with SensitivityCubeHDF5Container(filename, mode="w"):
            pass
    else:
        # Test explicitly closing
        hdcon = SensitivityCubeHDF5Container(filename, mode="w")
        hdcon.close()

    # Can we open it again?
    hdcon2 = SensitivityCubeHDF5Container(filename, mode="r")
    hdcon2.close()
    

@pytest.mark.parametrize('flush', [True, False])
def test_hdf5_add_extract(hdf5_container, sensitivity_cube, flush):
    """
    Test the adding and extracting of 
    sensitivity cubes into HDF5 
    """

    # Try adding it
    hdf5_container.add_sensitivity_cube("shot_19690720v11", "ifuslot_000", 
                                        sensitivity_cube, flush=flush)

    # Try getting it back again
    scube = hdf5_container.extract_ifu_sensitivity_cube("ifuslot_000")

    # Check it's the same
    vals_new = scube.f50vals.flatten() 
    vals_old = sensitivity_cube.f50vals.flatten() 

    assert vals_new == pytest.approx(vals_old)



