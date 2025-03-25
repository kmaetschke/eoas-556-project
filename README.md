# Satellite altimetry-derived gravimetry inversion at Kolumbo volcano
Project for the course EOAS 556 at UBC (Lecturer: Lindsey Heagy)

### Summary:
Submarine volcanic systems can pose significant hazards to inhabited coastal areas. Their location makes them
poorly accessible for geophysical surveys, which is why for most submarine volcanoes the plumbing systems and
eruptive mechanisms are not yet well understood. At subaerial volcanoes, gravimetry is widely used to infer magma
storage zones by detecting low-density anomalies. For submarine volcanoes, Vertical Gravity Gradient (VGG) data
derived from satellite radar altimetry can be used analogously.
Kolumbo submarine volcano, located in the southern Aegean 7 km northeast of the island of Santorini, Greece,
erupted catastrophically in 1650, creating a tsunami (Karstens et al., 2023). A potential renewed eruption would
be a large threat to the heavily populated Santorini island. Knowledge about the magma storage system can help
in assessing the volcanic hazard. 
In this project I am using publicly available satellite altimetry VGG data to infer the location of a
possible magma storage chamber under Kolumbo volcano.

### Data:
The used data sets for global Vertical Gravity Gradients with 1 arcminute resolution are available at https://topex.ucsd.edu/pub/global_grav_1min/ (Sandwell et al., 2014). They combine data from the altimeters Altika, Cryosat LRM,
Cryosat SAR, Sentinel-3A/B, Jason-2, and Cryosat-2.
For the corrections of the gravimetry data I use bathymetry data from GEBCO (https://download.gebco.net, GEBCO Bathymetric Compilation
Group 2022).

### Methods:
The method for using VGG data derived from satellite altimetry has been described by Le Mével (2024) and used
to create a model of the magmatic system of Hunga volcano (Le Mével et al., 2023). 
VGG data is sensitive to sufficiently small-scale anomalies, since it is the first vertical derivative of the
vertical gravity component.
The VGG data from Sandwell et al. (2014) needs to be corrected for the VGG gravity effect of the sea water and
bathymetry to achieve a Bouguer VGG anomaly. The regional gravity field then needs to be substracted, which
yields a residual Bouguer anomaly. This corrected data is then used to perform a 3-D gravity inversion with SimPEG (Heagy et al.,
2023).
These steps are all included in the Jupyter Notebook _gravity_gradient_inversion_ in this repository.


#### References: 
GEBCO Bathymetric Compilation Group 2022. (2022). The GEBCO2022 Grid - a continuous terrain model
of the global oceans and land [Dataset]. NERC EDS British Oceanographic Data Centre NOC. Retrieved from
https://www.gebco.net/data and products/gridded bathymetry data/gebco 2022/

Heagy, L., Capriotti, J., Kang, S., Astic, T., Fournier, D., Cowan, D. C., et al. (2023). simpeg/simpeg: V0.19.0
March 16, 2025 [Software]. Zenodo. Retrieved from https://docs.simpeg.xyz/v0.19.0/content/release/index.html

Karstens, J., Crutchley, G. J., Hansteen, T. H., Preine, J., Carey, S., Elger, J., K¨uhn, M., Nomikou, P., Schmid,
F., Dalla Valle, G., Kelfoun, K., & Berndt, C. (2023). Cascading events during the 1650 tsunamigenic eruption of
Kolumbo volcano. Nature Communications, 14(1), 6606. https://doi.org/10.1038/s41467-023-42261-y

Le Mével, H., Miller, C. A., Rib´o, M., Cronin, S., & Kula, T. (2023). The magmatic system under Hunga volcano
before and after the 15 January 2022 eruption. Science Advances, 9(50), eadh3156. https://doi.org/10.1126/
sciadv.adh3156

Le Mével, H. (2024). Imaging Magma Reservoirs From Space With Altimetry-Derived Gravity Data. AGU Ad-
vances, 5(6), e2024AV001403. https://doi.org/10.1029/2024AV001403

Sandwell, D. T., M¨uller, R. D., Smith, W. H. F., Garcia, E., & Francis, R. (2014). New global marine grav-
ity model from CryoSat-2 and Jason-1 reveals buried tectonic structure. Science, 346(6205), 65–67. https:
//doi.org/10.1126/science.1258213
