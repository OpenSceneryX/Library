Checklist for New Items
=======================

0. Investigate copyright

1. Check object origin - tip of nose for vehicles, centred for most other objects - on all LOD layers

2. Check object size

3. Check orientation - pointing North - on all LOD layers for vehicles

4. If object rotates in the wind, check it is aligned with the wind (straight down in WED) when rotated 0° (default). Also ensure it has the new WED directive to lock rotation: `#fixed_heading <deg>`

5. Convert to v8 format?

6. Remove any baked-in ground shadows

7. Check lit texture - new submissions shouldn't have baked in spill lighting effects, illuminated windows etc are ok

8. Check any PNGs are RGB, not indexed (X-Plane has a problem rendering indexed PNGs with a background colour as transparent)

9. Check texture size and check powers of 2, scale down if appropriate

10. Run textures through ImageOptim

11. If `info.txt` has been supplied, check line endings are UNIX

12. Create screenshot (automatically using script if desired)

13. Run `screenshot.jpg` through 'Process Screenshot' if not using generation script

14. Build library

15. Add to release notes

16. Tweet

17. Commit