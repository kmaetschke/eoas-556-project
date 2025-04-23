import numpy as np

# for mesh, forward modeling and inversion
from discretize import TreeMesh
from discretize.utils import mkvc, refine_tree_xyz, active_from_xyz
from simpeg.utils import plot2Ddata, model_builder
from simpeg import maps
from simpeg.potential_fields import gravity
from simpeg import (
    maps,
    data,
    data_misfit,
    inverse_problem,
    regularization,
    optimization,
    directives,
    inversion,
    utils,
)
import choclo


#function for creating a mesh
def create_gravity_mesh(dx, dy, dz, grav_east, grav_north, pad_x, pad_y, z_length):
    """
    Create a TreeMesh for gravity inversion with refinement below measurement points.
    
    Parameters
    ----------
    dx, dy, dz : float
        Minimum cell width (base mesh cell width) in x, y, z directions (meters)
    grav_east, grav_north : array-like
        Arrays of measurement point coordinates in easting and northing
    pad_x, pad_y : float
        Padding distance in x and y directions (meters)
    z_length : float
        Domain width in z direction (meters)
        
    Returns
    -------
    mesh : discretize.TreeMesh
        The created mesh object with refinement
    """
    # Calculate center of measurement points
    center_meas_x = np.min(grav_east) + (np.max(grav_east) - np.min(grav_east)) / 2.0
    center_meas_y = np.min(grav_north) + (np.max(grav_north) - np.min(grav_north)) / 2.0
    
    # Set mesh limits
    mesh_min_x = np.min(grav_east) - pad_x
    mesh_max_x = np.max(grav_east) + pad_x
    mesh_min_y = np.min(grav_north) - pad_y
    mesh_max_y = np.max(grav_north) + pad_y
    
    # Calculate domain widths
    x_length = mesh_max_x - mesh_min_x
    y_length = mesh_max_y - mesh_min_y
    
    # Compute number of base mesh cells
    nbcx = 2 ** int(np.round(np.log(x_length / dx) / np.log(2.0)))
    nbcy = 2 ** int(np.round(np.log(y_length / dy) / np.log(2.0)))
    nbcz = 2 ** int(np.round(np.log(z_length / dz) / np.log(2.0)))
    
    # Recalculate domain widths for symmetry
    x_length = nbcx * dx
    y_length = nbcy * dy
    z_length = nbcz * dz
    
    # Recalculate mesh limits for centered measurements
    mesh_min_x = center_meas_x - x_length / 2.0
    mesh_min_y = center_meas_y - y_length / 2.0
    
    # Define base mesh
    hx = [(dx, nbcx)]
    hy = [(dy, nbcy)]
    hz = [(dz, nbcz)]
    mesh = TreeMesh([hx, hy, hz], x0=[mesh_min_x, mesh_min_y, -z_length])
    
    # Set padding for refinement
    padding = [[2,2,2], [2,2,2]]
    
    # Refine mesh below data points
    xp, yp, zp = np.meshgrid(
        [np.min(grav_east)-(pad_x/2), np.max(grav_east)+(pad_x/2)],
        [np.min(grav_north)-(pad_y/2), np.max(grav_north)+(pad_y/2)],
        [-10000,0]
    )
    box = np.c_[mkvc(xp), mkvc(yp), mkvc(zp)]
    mesh.refine_bounding_box(box, padding_cells_by_level=padding, finalize=False)
    
    mesh.finalize()
    return mesh

# function for creating a synthetic model (with or without a spherical anomaly)
def create_density_model(mesh, xyz_topo, background_density=0.0, include_sphere=False,
                        sphere_density=-0.3, sphere_depth=-3000.0, sphere_radius=1500.0):
    """
    Create a density model with an optional spherical anomaly for gravity inversion.
    
    Parameters
    ----------
    mesh : discretize.TreeMesh
        The mesh object for the model
    xyz_topo : array-like
        Surface topography points (n, 3) array
    background_density : float, optional
        Background density in g/cc (default: 0.0)
    include_sphere : bool, optional
        Whether to include a spherical anomaly (default: True)
    sphere_density : float, optional
        Density of spherical anomaly in g/cc (default: -0.3)
    sphere_depth : float, optional
        Depth of sphere center in meters (default: -3000.0)
    sphere_radius : float, optional
        Radius of sphere in meters (default: 1500.0)
    
    Returns
    -------
    tuple
        Contains:
        - true_model : array-like
            Density model values for active cells
        - ind_active : array-like
            Boolean array indicating active cells
        - model_map : maps.IdentityMap
            Mapping from model to active cells
    """
    # Find active cells (below topography)
    ind_active = active_from_xyz(mesh, xyz_topo)
    
    # Create mapping from model to active cells
    nC = int(ind_active.sum())
    model_map = maps.IdentityMap(nP=nC)
    
    # Initialize model with background density
    true_model = background_density * np.ones(nC)
    
    if include_sphere:
        # Find center of measurement points for sphere placement
        center_meas_x = (np.min(mesh.cell_centers_x) + np.max(mesh.cell_centers_x)) / 2.0
        center_meas_y = (np.min(mesh.cell_centers_y) + np.max(mesh.cell_centers_y)) / 2.0
        
        # Add spherical anomaly
        ind_sphere = model_builder.get_indices_sphere(
            np.r_[center_meas_x, center_meas_y, sphere_depth],
            sphere_radius,
            mesh.gridCC
        )
        ind_sphere = ind_sphere[ind_active]
        true_model[ind_sphere] = sphere_density
    
    return true_model, ind_active, model_map