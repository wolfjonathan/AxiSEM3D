# AxiSEM3D Release Task List

This is to be followed loosely and likely needs small adaption in
every release. The only important step is bumping the version info in
a single commit and tagging this commit.

1. determine new version roughly following semantic versioning: http://semver.org/
  - format is X.Y.Z for a release, X.Y.Z-pre for the dev version or X.Y.Z-rcW for release candidates
  - backwards incompatible changes require incrementing X, adding features incrementing Y
```
  export VERSION=2.1.0
  export VERSIONSHORT=2.1
  export NEXTVERSION=2.2.0-pre
  export TAG=v${VERSION}
```

2. Create a PR to update changelog for release, add header for current release - wait for merge

3. Create branch axisem3d-${VERSIONSHORT} (or checkout current one if minor point release)

4. Bump version and tag the release:
```
  ./tools/release/bump_version.sh ${VERSION}
  git commit -m "version ${VERSION}"
  git tag -s $TAG -m "version $TAG"
```

5. Make public (branch and tag):

  ```
  git push upstream axisem3d-$VERSIONSHORT
  git push upstream $TAG
  ```

6. Update main:
```
  git checkout -b post-release-${VERSION} upstream/main
  ./tools/release/bump_version.sh ${NEXTVERSION}
```
and make a PR.

7. Create a new version on Zenodo

8. Create release on Github: https://github.com/AxiSEMunity/AxiSEM3D/releases/new
   - include changelog
   - include link to https://axisem3d.readthedocs.io/ (pick release)
   - include zenodo link

9. Celebrate!
