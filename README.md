# Satellite altimetry-derived gravity gradient inversion at Kolumbo volcano
Project for the course EOAS 556 at UBC (Lecturer: Lindsey Heagy)

### Summary:
Submarine volcanic systems can pose significant hazards to inhabited coastal areas. Their
location makes them poorly accessible for geophysical surveys, which is why for most
submarine volcanoes the plumbing systems and eruptive mechanisms are not yet well
understood. At subaerial volcanoes, gravimetry is widely used to infer magma storage zones
by detecting low-density anomalies. For submarine volcanoes, gravity data derived from
satellite measurements can be used analogously.
Kolumbo submarine volcano, located in the southern Aegean 7 km northeast of the island
of Santorini, Greece, erupted catastrophically in 1650, creating a tsunami (Karstens et al.,
2023). A potential renewed eruption would be a large threat to Santorini island. Knowledge
about the magma storage system can help in assessing the volcanic hazard. I use publicly
available gravity disturbance data to attempt to infer the location of a possible magma
storage chamber under Kolumbo volcano.

### Data:
The used data sets for global gravity disturbances are available at https://icgem.gfz-potsdam.de/calcgrid (Ince et al. 2019). I use the EIGEN-6C4 gravity disturbance in a 1 arc-minute grid and geoid in a 15 arc-second grid.<br>
For the corrections of the gravity data I use bathymetry data from GEBCO (https://download.gebco.net, GEBCO Compilation Group (2024) GEBCO 2024 Grid (doi:10.5285/1c44ce99-0a0d-5f4f-
e063-7086abc0ea0f)).
For the corrections, I further use the CRUST1.0 model (https://ds.iris.edu/ds/products/emc-crust10/) (Laske et al., 2013).

### Methods:
The method for correcting gravity disturbance data has been described by a Fatiando a Terra tutorial (Soler et al. 2021).
The gravity disturbance needs to be corrected for the gravity effect of the bathymetry and topography to achieve a Bouguer graviyt disturbance. The regional gravity field then needs to be substracted, which yields a residual disturbance. This corrected data is then used to perform a 3-D gravity inversion with SimPEG (Heagy et al.,
2023).

### Installation instructions:
1. Download the data from the sources described under 'Data'
2. Run the notebook gravity_processing.ipynb to correct the gravity disturbance data as described above.
3. Then, with the corrected data, run the notebook gravity_inversion.ipynb
The included environment.yml file in the repository should help in runnning the provided code locally.

#### References: 
Heagy, L., Capriotti, J., Kang, S., Astic, T., Fournier, D., Cowan, D. C., et al. (2023). simpeg/simpeg: V0.19.0
March 16, 2025 [Software]. Zenodo. Retrieved from https://docs.simpeg.xyz/v0.19.0/content/release/index.html

Ince, E. Serkan et al. (2019): ICGEM – 15 years of successful collection and distribution of global
gravitational models, associated services and future plans. DOI: 10.5194/essd-11-647-2019.
URL: http://doi.org/10.5194/essd-11-647-2019.

Karstens, J., Crutchley, G. J., Hansteen, T. H., Preine, J., Carey, S., Elger, J., K¨uhn, M., Nomikou, P., Schmid,
F., Dalla Valle, G., Kelfoun, K., & Berndt, C. (2023). Cascading events during the 1650 tsunamigenic eruption of
Kolumbo volcano. Nature Communications, 14(1), 6606. https://doi.org/10.1038/s41467-023-42261-y

Laske, Gabi et al. (2013): “Update on CRUST1.0 – A 1-degree Global Model of Earth’s Crust”.
In: Geophysical Research Abstracts. Vol. 15. Abstract presented at EGU General Assembly
2013, EGU2013–2658

Soler, Santiago et al. (2021): Processing and gridding gravity data with Fatiando a Terra. URL:
https://www.fatiando.org/tutorials/notebooks/gravity-processing.html#reference-heights-
to-the-ellipsoid.

