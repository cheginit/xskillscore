import numpy as np
import pytest
import xarray as xr

PERIODS = 12  # effective_p_value produces nans for shorter periods

np.random.seed(42)


@pytest.fixture
def times():
    return xr.cftime_range(start="2000", periods=PERIODS, freq="D")


@pytest.fixture
def lats():
    return np.arange(4)


@pytest.fixture
def lons():
    return np.arange(5)


@pytest.fixture
def members():
    return np.arange(3)


# o vs. f in probabilistic
@pytest.fixture
def o(times, lats, lons):
    """Observation."""
    data = np.random.rand(len(times), len(lats), len(lons))
    return xr.DataArray(
        data,
        coords=[times, lats, lons],
        dims=["time", "lat", "lon"],
        attrs={"source": "test"},
    )


@pytest.fixture
def f_prob(times, lats, lons, members):
    """Probabilistic forecast containing also a member dimension."""
    data = np.random.rand(len(members), len(times), len(lats), len(lons))
    return xr.DataArray(
        data,
        coords=[members, times, lats, lons],
        dims=["member", "time", "lat", "lon"],
        attrs={"source": "test"},
    )


@pytest.fixture
def f(f_prob):
    """Deterministic forecast matching observation o."""
    return f_prob.isel(member=0, drop=True)


# a vs. b in deterministic
@pytest.fixture
def a(o):
    return o


@pytest.fixture
def b(f):
    return f


# nan
@pytest.fixture
def a_rand_nan(a):
    """Masked"""
    return a.where(a < 0.5)


@pytest.fixture
def b_rand_nan(b):
    """Masked"""
    return b.where(b < 0.5)


@pytest.fixture
def a_fixed_nan(a):
    """Masked block"""
    a.data[:, 1:3, 1:3] = np.nan
    return a


@pytest.fixture
def b_fixed_nan(b):
    """Masked block"""
    b.data[:, 1:3, 1:3] = np.nan
    return b


# with zeros
@pytest.fixture
def a_with_zeros(a):
    """Zeros"""
    return a.where(a < 0.5, 0)


# dask
@pytest.fixture
def a_dask(a):
    """Chunked"""
    return a.chunk()


@pytest.fixture
def b_dask(b):
    """Chunked"""
    return b.chunk()


@pytest.fixture
def a_rand_nan_dask(a_rand_nan):
    """Chunked"""
    return a_rand_nan.chunk()


@pytest.fixture
def b_rand_nan_dask(b_rand_nan):
    """Chunked"""
    return b_rand_nan.chunk()


@pytest.fixture
def o_dask(o):
    return o.chunk()


@pytest.fixture
def f_prob_dask(f_prob):
    return f_prob.chunk()


# 1D time
@pytest.fixture
def a_1d(a):
    """Timeseries of a"""
    return a.isel(lon=0, lat=0, drop=True)


@pytest.fixture
def b_1d(b):
    """Timeseries of b"""
    return b.isel(lon=0, lat=0, drop=True)


@pytest.fixture
def a_1d_fixed_nan():
    time = xr.cftime_range("2000-01-01", "2000-01-03", freq="D")
    return xr.DataArray([3, np.nan, 5], dims=["time"], coords=[time])


@pytest.fixture
def b_1d_fixed_nan(a_1d_fixed_nan):
    b = a_1d_fixed_nan.copy()
    b.values = [7, 2, np.nan]
    return b


@pytest.fixture
def a_1d_with_zeros(a_with_zeros):
    """Timeseries of a with zeros"""
    return a_with_zeros.isel(lon=0, lat=0, drop=True)


# weights
@pytest.fixture
def weights_cos_lat(a):
    """Weighting array by cosine of the latitude."""
    return xr.ones_like(a) * np.abs(np.cos(a.lat))


@pytest.fixture
def weights_lonlat(a):
    weights = np.cos(np.deg2rad(a.lat))
    _, weights = xr.broadcast(a, weights)
    return weights.isel(time=0, drop=True)


@pytest.fixture
def weights_time():
    time = xr.cftime_range("2000-01-01", "2000-01-03", freq="D")
    return xr.DataArray([1, 2, 3], dims=["time"], coords=[time])


@pytest.fixture
def weights_cos_lat_dask(weights_cos_lat):
    """
    Weighting array by cosine of the latitude.
    """
    return weights_cos_lat.chunk()


@pytest.fixture
def category_edges():
    """Category bin edges between 0 and 1."""
    return np.linspace(0, 1 + 1e-8, 6)
