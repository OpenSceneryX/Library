Release Howto
=============

0. Pre-build the library

    ```bash
    $ python3 build.py
    ```

1. Check the build for missing virtual paths

    ```bash
    $ python3 check.py
    ```

2. Create release branch

3. Update release notes to include version and date

4. Update "Enhanced By" logo to correct version number, export as PNG and run through ImageOptim

5. Commit release changes, tag and merge release changes back into develop

6. Clean target folder and build library

    ```bash
    $ python3 build.py
    ```

    ENSURE 'y' is selected for 'Build PDF'

7. Zip the built `OpenSceneryX-x.x.x` folder as `OpenSceneryX-x.x.x.zip`:

    ```bash
    $ export COPYFILE_DISABLE=true
    $ zip -r OpenSceneryX-x.x.x.zip OpenSceneryX-x.x.x
    ```

8. Run Manifester on built `OpenSceneryX-x.x.x` folder and save `manifest.xml`

9. Zip `manifest.xml` using the command line

    ```bash
    $ zip manifest.xml.zip manifest.xml
    ```

10. Run Packager

    ```bash
    $ python3 package.py
    ```

11. Zip `OpenSceneryX-Website-x.x.x/` and `OpenSceneryX-DeveloperPack-x.x.x/`

    ```bash
    $ zip -r OpenSceneryX-Website-x.x.x.zip OpenSceneryX-Website-x.x.x
    $ zip -r OpenSceneryX-DeveloperPack-x.x.x.zip OpenSceneryX-DeveloperPack-x.x.x
    ```

12. Clear `/new/` and `/old/` on the server

13. Upload `OpenSceneryX-Website-x.x.x.zip` into `/new/`:

    ```bash
    $ scp OpenSceneryX-Website-x.x.x.zip <server>:<path>/new/
    ```

14. Upload the following into AWS S3 Bucket:

    - `OpenSceneryX-DeveloperPack-x.x.x.zip`
    - Monolithic zip file `OpenSceneryX-x.x.x.zip`
    - `manifest.xml.zip`

15. Use AWS cli to sync the new repository:

    ```bash
    $ cd OpenSceneryX-x.x.x/
    $ aws s3 sync . s3://opensceneryx/repository
    ```

16. Ensure AWS S3 permissions on the following are public:

    - `OpenSceneryX-DeveloperPack-x.x.x.zip`
    - Monolithic zip file `OpenSceneryX-x.x.x.zip`
    - `manifest.xml.zip`
    - `/repository`

17. In AWS Cloudfront console, create invalidatation in downloads.opensceneryx.com distribution for:

    ```txt
    /repository/*
    /manifest.xml.zip
    ```

18. Extract website zip on site into `/new/`

    ```bash
    $ unzip OpenSceneryX-Website-x.x.x.zip
    ```

19. Put site into maintenance mode

    ```bash
    $ mv wp/maintenance-disabled wp/.maintenance
    ```

20. Move `/doc/`, `/extras/`, `/facades/`, `/forests/`, `/lines/`, `/objects/`, `/polygons/`, `/library-sitemap.xml` and `robots.txt` from webroot into `/old/`

    ```bash
    $ mv doc ../old/ && mv extras ../old/ && mv facades ../old/ && mv forests ../old/ && mv lines ../old/ && mv objects ../old/ && mv polygons ../old/ && mv library-sitemap.xml ../old/ && mv robots.txt ../old/
    ```

21. Move `/new/OpenSceneryX-Website-x.x.x/*` to webroot

22. Ensure `/versioninfo` has the latest information about the installer in it.

23. Correct ownership of folder structure

    ```bash
    $ chown -R apache:apache public_html
    ```

24. Take site out of maintenance mode

    ```bash
    $ mv wp/.maintenance wp/maintenance-disabled
    ```

25. Log into Cloudflare and clear all caches.

26. Log in to Google Search Console and resubmit `library-sitemap.xml`

27. Log in to Bing Webmaster tools and resubmit `library-sitemap.xml`

28. Create new section in release note for next changes

29. Promotion:

    - Update [x-plane.org Download Manager entry](https://forums.x-plane.org/index.php?/files/file/2226-opensceneryx/)
    - Update first post in [x-plane.org main OpenSceneryX thread](https://forums.x-plane.org/index.php?/forums/topic/25174-opensceneryx-v320-released/)
    - Create a new post in the [x-plane.org 'General' forum](https://forums.x-plane.org/index.php?/forums/forum/1-general-x-plane-forum/) and request transfer to 'News' forum
    - Create a new post in the thresholdx.net 'OpenSceneryX Announcements' forum
    - Post an article on opensceneryx.com
    - Tweet
    - Reddit r/Xplane

30. Drop `library.txt` into Backup Library project

31. If any new items are part of a third party library, then create / update the special opensceneryx file within that library in the Backup Library project

