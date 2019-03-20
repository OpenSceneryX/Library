Checklist for New Items
=======================

0. Investigate copyright

1. Check object origin - tip of nose for vehicles, centred for most other objects - on all LOD layers

2. Check object size

3. Check orientation - pointing North - on all LOD layers for vehicles

4. If object rotates in the wind, check it is aligned with the wind (straight down in WED) when rotated 0° (default). Also ensure it has the new WED directive to lock rotation: `#fixed_heading <deg>`

5. If item supports seasonal variants and contains snow, it is important to export both `winter_snow` and `winter_deep_snow` variants, even if they are the same. This is to ensure that plugins that support both modes show snowy items in both cases as they are mutually exclusive. `winter` is used for common items across both snow and no snow (e.g. grass that disappears), `winter_no_snow` is obviously used for bare winter variants without snow.

6. Convert to v8 format?

7. Remove any baked-in ground shadows

8. Check lit texture - new submissions shouldn't have baked in spill lighting effects, illuminated windows etc are ok

9. Check any PNGs are RGB, not indexed (X-Plane has a problem rendering indexed PNGs with a background colour as transparent)

10. Check texture size and check powers of 2, scale down if appropriate

11. Run textures through ImageOptim

12. If `info.txt` has been supplied, check line endings are UNIX

13. Create screenshot (automatically using script if desired)

14. Run `screenshot.jpg` through 'Process Screenshot' if not using generation script

15. Build library

16. Add to release notes

17. Tweet

18. Commit