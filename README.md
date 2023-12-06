# Welcome!
This repository contains the code examples of the book "Einführung in Optimierungsmodelle" (Sudermann-Merx, 2023).

<p align="center">
  <img src="https://github.com/spiralulam/intro_opt_models/assets/45530936/b7b915bf-fc19-4ae1-98d3-8801c3c730fc" width=33% height=33%>
</p>

# Further remarks
- A list of errata can be found [here](errata.md).
- If you are a Mac User with an M1 or M2 chip you will face problems with the installation of `python-mip`, in particular
  with the CBC solver. 
  [tuliotoffolo](https://github.com/tuliotoffolo) promised to look into it by the end of 2023. Big thanks to 
  [kochersg](https://github.com/kochersg) for finding a temporary workaround (see
  [this](https://groups.google.com/g/python-mip/c/0R2NC_URD6M) discussion and in particular Tom Schlomo's answer. On Mac 
  the package `bash 4` is needed which can be installed using `homebrew install bash`.