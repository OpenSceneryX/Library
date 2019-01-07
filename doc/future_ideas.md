Future Ideas List
=================

Installer
---------

* Handle both PNG and DDS textures when present.

* Detect which objects are used in the user's installed scenery packages, and only install those.

  - Get server manifest full list.

  - Parse DSFs & build list of used files if option selected.

  - Reduce server manifest list to just those files required.

  - Compare with local manifest.

  - Generate library.txt file.

  - Add in standard files like Readme.

  - Problem - DSF only contains references to .obj, .fac etc, not the textures they use.  Will need
    to build a more extended manifest file containing all referenced files.

  - Check it works after changing X-Plane folders.

* Split library into multiple, optional packages.

* User agent should include platform.


Library
-------

* Split library into multiple, optional packages


Website
-------

* The sub-categories section of category landing pages should be better
  - Perhaps there should be a selection of random images for each category
  - Or create custom folder icons for each type of item e.g. cube on a folder for objects
  - Or use the screenshot for the first item in the folder as the folder icon

* Handle formatted info.txt content better (e.g. Cormac's comments).

* Mark whether an object has a lit texture.

* 3D renderer for x-plane .obj files.

* Add more info to facade, forest and line pages in the same way that the polygon and object pages show extended info.

* Page listing which libraries are integrated with OSX: RE_Library, FlyAgi_Vegetation, FlyAgi_Wind_Turbines
