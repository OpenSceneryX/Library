# Introduction

We are always looking for new contributions to the library – buildings, static aircraft, ground markings or anything else you would like to contribute. Also, check the GitHub outstanding issues list for tasks which you could help with.

# Copyright on Contributions

If you want to become a contributor, you must agree that your work can be distributed to anyone who downloads the library, under the [Creative Commons Attribution-Noncommercial-No Derivative Works 3.0](https://creativecommons.org/licenses/by-nc-nd/3.0/) License.  In addition, if you have included any work from anyone else then they must give their permission too.  We will contact them if you wish, but you must make this clear and let us know their contact details.  A couple of examples of where this is necessary:

1. Where you have converted an X-Plane aircraft into a static object, you must get permission from the original author of the aircraft.
1. Where someone else owns the copyright for the original photograph that a texture is based on, then they must give permission.

Note that the Creative Commons license protects against people copying objects out of the library and distributing them as part of their own work.  However, there are no restrictions on who can reference objects from the library – so for example OpenSceneryX can legally be used by payware authors, as the payware author is not distributing your work to the end user, we are.

You must also agree not to get upset if your submission is declined – Now that the library has reached a decent size, we are getting stricter on quality control so don’t be upset if we have some suggestions for improvements before your stuff is added.

# Standards for Contributions

There are a few standards and checks that you should do before submitting, otherwise we may ask you to fix these:

1. Please ensure the scaling of the object is correct. For example, in [Blender](https://www.blender.org) 1 unit = 1 meter.
1. If it’s an object with an identifiable ‘nose’ (like an aircraft, car, boat etc.) then please align the object pointing North with the tip of its nose at the origin (0, 0) – zoom in in your 3d editor to position it exactly.
1. If the object doesn’t have an identifiable nose then please centre the object on the origin (0, 0). This includes buildings.
1. If your contribution includes lighting, please use the lighting model which was introduced in X-Plane® 10, so do not include baked-in ground shadows and spill lighting effects in textures. You can still include illuminated internal elements, for example windows, but where it is possible to use a proper X-Plane® light source, please do so.
1. Please spend some time optimising your object model and textures. Remember that everyone worldwide who uses OpenSceneryX will have to download your object, so the smaller and more efficient you can make it the better!

# How To Submit

## If you are contributing content (i.e. X-Plane® objects, facades etc.)

1. Please put every item in its own folder. Put any textures the object uses in the same folder as the object… unless…
1. If any textures are shared between multiple objects, please put the textures in their own folder.
1. Locate your content somewhere you think sensible in the library. Get in touch if you don't know where the best place would be.
1. Please include in the pull request a list of all third parties that own copyright on any part of your contribution. You can also supply some background information about the object too if you wish. If you want to be really helpful, there is a standard format that we use for these read-me files. In this standard format, the file is named info.txt. Click here for a template file and click here to see an example of a completed file.

## If you are contributing anything else (code, other improvements, working on an issue)

Please get in touch before you start work, we can discuss approach and objectives.

## Or – Do you have a whole library you would like to merge with OpenSceneryX?

We have recently been accepting full library merges, where an existing library is merged into OpenSceneryX in its entirety. This involves a lot of work on our side, so if you are the owner of an existing library and would like to donate it, please get in touch so we can discuss.
