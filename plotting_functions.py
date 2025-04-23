import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import cmocean

def plot_gravity_comparison(bathymetry_ellips, grav_east, grav_north, grav_proj, gravity_bouguer_mgal,
                          cbar1_label="height above reference ellipsoid",
                          cbar2_label="gravity disturbance (mGal)",
                          title1="Gravity Disturbance",
                          title2="Bouguer Gravity Disturbance",
                          shared_cbar=False,
                          cbar1_data='bathymetry',
                          cbar2_data='scatter'):
    """
    Create a figure with two subplots showing gravity disturbance and Bouguer gravity disturbance.
    
    Parameters
    ----------
    bathymetry_ellips : xarray.DataArray
        Bathymetry data relative to reference ellipsoid
    grav_east : array-like
        Easting coordinates of gravity measurements
    grav_north : array-like
        Northing coordinates of gravity measurements
    grav_proj : array-like
        Gravity disturbance values
    gravity_bouguer_mgal : array-like
        Bouguer gravity disturbance values
    cbar1_label : str, optional
        Label for the first colorbar
    cbar2_label : str, optional
        Label for the second colorbar
    title1 : str, optional
        Title for the first subplot
    title2 : str, optional
        Title for the second subplot
    shared_cbar : bool, optional
        If True, scatter plots share the same colorbar range
    cbar1_data : str, optional
        Which data to use for first colorbar ('bathymetry' or 'scatter')
    cbar2_data : str, optional
        Which data to use for second colorbar ('bathymetry' or 'scatter')
    
    Returns
    -------
    fig : matplotlib.figure.Figure
        The created figure
    """
    
    # Create figure with GridSpec
    fig = plt.figure(figsize=(11, 7))
    gs = gridspec.GridSpec(2, 2, height_ratios=[1, 0.05])
    gs.update(hspace=0.25, wspace=0.2)
    
    # Create main subplot axes and colorbar axes
    ax1 = plt.subplot(gs[0, 0])
    ax2 = plt.subplot(gs[0, 1], sharex=ax1, sharey=ax1)
    cax1 = plt.subplot(gs[1, 0])
    cax2 = plt.subplot(gs[1, 1])
    
    # Set up color ranges for scatter plots
    if shared_cbar:
        vmin = min(np.min(grav_proj), np.min(gravity_bouguer_mgal))
        vmax = max(np.max(grav_proj), np.max(gravity_bouguer_mgal))
    else:
        vmin1, vmax1 = np.min(grav_proj), np.max(grav_proj)
        vmin2, vmax2 = np.min(gravity_bouguer_mgal), np.max(gravity_bouguer_mgal)
    
    # First subplot
    cm1 = bathymetry_ellips.plot.pcolormesh(
        ax=ax1, cmap=cmocean.cm.topo, add_colorbar=False
    )
    sc1 = ax1.scatter(
        grav_east, grav_north, c=grav_proj, cmap='viridis', s=40, edgecolor='black',
        vmin=vmin if shared_cbar else vmin1,
        vmax=vmax if shared_cbar else vmax1
    )
    
    # Set colorbar for first subplot based on choice
    if cbar1_data == 'bathymetry':
        cbar1 = fig.colorbar(cm1, cax=cax1, orientation='horizontal', aspect=40)
    else:  # 'scatter'
        cbar1 = fig.colorbar(sc1, cax=cax1, orientation='horizontal', aspect=40)
    cbar1.set_label(cbar1_label)
    ax1.set_xlabel('Easting (m)')
    ax1.set_ylabel('Northing (m)')
    ax1.set_title(title1)
    
    # Second subplot
    cm2 = bathymetry_ellips.plot.pcolormesh(
        ax=ax2, cmap=cmocean.cm.topo, add_colorbar=False
    )
    sc2 = ax2.scatter(
        grav_east, grav_north, c=gravity_bouguer_mgal, cmap='viridis', s=40, 
        edgecolor='black',
        vmin=vmin if shared_cbar else vmin2,
        vmax=vmax if shared_cbar else vmax2
    )
    
    # Set colorbar for second subplot based on choice
    if cbar2_data == 'bathymetry':
        cbar2 = fig.colorbar(cm2, cax=cax2, orientation='horizontal', aspect=40)
    else:  # 'scatter'
        cbar2 = fig.colorbar(sc2, cax=cax2, orientation='horizontal', aspect=40)
    cbar2.set_label(cbar2_label)
    ax2.set_xlabel('Easting (m)')
    ax2.set_ylabel('Northing (m)')
    ax2.set_title(title2)
    
    return fig