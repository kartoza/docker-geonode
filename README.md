# GeoNode Container Image Builder

This repository is used to make a GeoNode docker build variants.

# How to use

Docker image will be built automatically using Github action for several branches and tags.
Image will be available in [Docker Hub](https://hub.docker.com/repository/docker/kartoza/geonode).
Any project specific image will be stored on each Docker Hub repo for it's own project.
This git repository will store each project specific recipe in it's own branch in this repo.
Customized recipe will be stored there, together with it's dependency declarations.

The following section contains information and convention on how to use the project structures
to manage several independent build sharing builders code between branches.

The main motivation on using this kind of structures is to allow independent build between branches,
without having to be blocked by upstream changes. If we can make a quick bugfix in a specific branches,
do it in that branch instead of having to require to push the commit to upstream branch. We can
also pull changes from other branches without having to wait from their approval. Lastly,
we can send patches to upstream branches via PR.

## Standard Naming conventions

### Terminologies

In order to easily recognize and express dependencies, we introduce some extra terminologies/words:

- `main_app_version`: The software version, in this case, solely GeoNode version.
- `app_version`: The software version, in this case, GeoNode (with any of it's related dependencies). Use SemVer convention. If extra versioning needed
  (for child dependencies), use pattern with slash and dash like this: `{main_app_version}/{component}-{component_version}`, for example: `3.1/mapstore-v2021.01.01`.
  With this rule, `main_app_version` and `app_version` can be the same if it's a vanilla one. For example `3.1` version of GeoNode.
- `component_version`: Optional. If we develop specific component version to be integrated with the image, then we express the component version too.
  The versioning scheme depends on the software/libraries being integrated.
- `version`: Note that the version in this repo here, refer to the version of the docker image **orchestration**, which is the recipes used to create said docker 
  image.  Developing the orchestration script or builder scripts happens in `main` and `develop` branch. Since it doesn't reflect to any feature based software, 
  Calendar versioning is used. Some example: `v2021.01.01`. Use dot instead of dash to allow regex match with SemVer.
- `main_project_name`: The customization name. It can be client project's name, or stack name. A vanilla GeoNode project can be considered empty string.
- `project_name`: The full project name. It contains pattern: `{main_project_name}-{project_name}`. It may expands if the projects/stacks have sub projects,
  for example: `{main_project_name}-{project_name}-{sub_project_name}`. 
  Each segment separated by dash/hyphen. `main_project_name` and singular `project_name` must not contain dash.

### Git Branch

This repository are arranged to have a main vanilla GeoNode image tracked in a `main` branch.
Any other branch are derived from that with separated overlay files to be embedded according to the customizations.
We arrange it this way in order to easily pull latest changes in `main` branch without conflicts.

Git branch to track main GeoNode release (the stable release) is `main` branch.
Git branch to track develop/latest GeoNode release goes to `develop` branch.

Git branch to track each project customized branch must have pattern `project-{project_name}`, where `project_name` refer to the name 
of the project where this GeoNode image will be used.

Any other branch besides that can be considered as one of the following:
- a test branch (can be discarded or ignored per usage)
- a test branch for PR (can be used to do CI/CD tests with image build automatically created using Github action)

### Git Tag

Git tag is used to pin exact commit of the branch as easily remembered shortname. This is useful to pin the build to the docker image build.

Git tag of the main GeoNode release uses the same tag scheme of the main GeoNode release, which is the `app_version`. For example: `3.0`, `3.1`, etc.

Git tag for specific project uses the `project_name` as the prefix. For example, `least_electrification-3.1` or `belfast-3.0`, etc.

Git tag with heavily customized version of the main branch must reflect the extensions in it's tag. For example, we have a GEP stack 
that extends from vanilla GeoNode. Then, we have a client project with specific customized version of said GEP stack. This means 
the `project_name` must express this, like `least_electrification-somalia-3.1`. Currently the pattern is a dash separated `project_name` with each `project_name` uses underscore
instead of dash to replace dash or space. Like this: `{main_project}-{sub_project}-{app_version}`, if the `sub_project` contains dash or spaces, 
like `Clean Cooking Alliance`, then convert it to `clean_cooking_alliance`.

Git tag must be immutable (ideally), in the sense that specific tag must map to a certain commit. Mapping change must be consciously approved.

Git tag of evolving generic branch should end with Calendar versioning of the orchestration. This is because we actually tracking the change of the 
orchestration/image builder. If we already have `least_electrification-3.1` and then the project itself is evolving (not a one time deliverable), then we should delete that tag 
(or mark it as deprecated) then replace it with the full `app_version` + `version`. So the git tag becomes: `{project_name}-{app_version}/{version}`, example: 
`least_electrification-somalia-3.1/gep-v1.1.14/v2021.01.01`. `version` has to be a suffix (the last), because it's the one who often changes. 
Component version can be specified after the `main_app_version`.

If the git tag coming from a branch `project-{project_name}` have a pattern `{project_name}/{version}`, then we call this the **canonical git tag**. For example,
`least_electrification-somalia/v2021.01.01`.

All the naming scheme above is used in order to be easily indexed and searched with regex. Simple release lookup for a project/stack can be done with just 
specifying the prefix, in this case the `project_name`. Git tag must be as canonical as possible because we want to use it as input for docker build.
Due to this reason, it is most recommended that we add the `version` segment.
`project_name` + `version` segments serves as a canonical map of the `project-{project_name}` branch's commit.
Adding `main_app_version` and `component_version` into the tag is mostly to make us easier to search/index it by version, and as a 
human readable version expression. For example, `least_electrification-somalia/v2021.01.01` is the canonical git tag for `project-least_electrification-somalia`
branch. However, it doesn't convey any information about what GeoNode version it is using and which GEP component version it is using.
Sometimes we need these information to easily know if a tag needs an update/new version.

If you need to build UI or CLI that leverages this git tag convention, consider using the following python regex:

```
^(?P<project_name>[\w-]+)-(?P<main_app_version>[v\d.]+)(/(?P<component>[\w.\-/]+))*(/(?P<version>[v\d.]+))$
```

It will match:
- `project_name`
- `main_app_version`
- `component`
- `version`

`project_name` have regex:

```
^(?P<main_project>\w+)(-(?P<sub_project>[\w\-]+))?$
```

It will match:
- `main_project`
- `sub_project` which is a dash separated token of sub project. Or, can be matched with regex `(\w+)` where it will match multiple groups.

`component` can be parsed with regex:

```
(?P<component_name>[\w]+)-(?P<component_version>[v\d.]+)
```

It will match multiple groups with named group:
- `component_name` the component name
- `component_version` the version of the component

You can think of `project_name` as a hierarchical organization of projects, from top to bottom.
`component` can be thought of as key value pair labels, so it can be used as filters because `component_version` supports value ordering.
This can be useful if you plan to build interfaces that can filter these git tags.
`version` and `main_app_version` is an ordered value. This can also be used as filters.

### Image Tag

Image tag is a tag used for our (Docker) container image.

Build source of an image tag may come from a branch or tag.

Multiple image tag may refer to the same commit build source. You can have `debian/3.1` and `alpine/3.1` built from the same git commit.

We explicitly do not allow monorepo based build source. A branch build can only build images for a specific project. This is to allow more independent build 
for any projects.

Image tag that uses HEAD of `main` branch should be tagged as `stable`.

Image tag that uses HEAD of `develop` branch should be tagged as `latest`.

Image tag that uses HEAD of `project-{project_main}` branch should be tagged as `{project_main}/latest`.

Image tag that uses canonical git tag of `{project_name}/{version}` should be tagged as `{project_name}/{version}`.

If the image repository is reserved to a `project_name`, then you should omit `project_name` from the image tag.
So, the image tag is just `{version}`. For example, normally the image repo is `kartoza/geonode`. 
So, a canonical git tag `sadc_gip/v2021.01.01` will have full image name: `kartoza/geonode:sadc_gip/v2021.01.01`.
However if you want to store the image in `kartoza/sadc_gip` repo, then the full image name is just `kartoza/sadc_gip:v2021.01.01` for brevity.

One build source commit may produce multiple image output (multiple different images or image variants).
Note that this is **different output** and not different-tag-but-same-image. 
For example, one commit source may produce one GeoNode image, and then the corresponding matching GeoServer image. This is two different images.
Another example, one commit source may produce one GeoNode image for debugging (with debug logging set up), and another one for production used (optimized).
Any other example, you may want to produce one GeoNode image but using a different image variant, like `debian` or `alpine`.

A `variant` is a slash separated unique name identifying the **kind** of image you produce. It must be ordered from generic to specific. For example,
you want to build GeoNode image, using debian base, but for debugging. The variant name for this case can be `debian/geonode/debug`. The logic for this order:

- `debian` is a base image (the base docker image)
- `geonode` is the software that you install on top of debian (build layer on top of debian)
- `debug` is the customization of GeoNode. Basically a term `debug` can't be a generic one, because you need to know what debug mode it applies to.
  You had to specify the software.
  
If any of the `variant` segment is unambigous, you can omit it for brevity. For example, if the `debian` image is a default base image, you can skip this segment. 
If you only build `geonode` image, you can skip this segment. Finally, if you only produce production mode image, you can omit `debug` segment. A rule of thumb, 
if you have two exact `variant` name, then just omit it. For example, if you have two variant `debian/geonode/debug` and `debian/geonode/prod` and nothing else, then you might as 
well just called it `debug` and `prod` variant.

If the image tag is in the form `{project_name}--{variant}/{version}` (note the double dash between `project_name` and `variant`), 
then we can call this the **canonical image tag**. For example, 
`least_electrification-somalia--debian/debug/v2021.01.01`. Canonical image tag may omit `project_name` if the image repo is unambigously reserved for that project 
only. In this case, the image tag is just `debian/debug/v2021.01.01` and the full image name may be like this: `kartoza/least_electrification-somalia:debian/debug/v2021.01.01`.

It is more recommended to express image dependencies and build source as image label and exclude it from the image tag. Convention for the image label will 
be specified later.

Other than rules specified above, you can implement your own image tag naming scheme if you need a shorthand tag. 
For example, you can specify in your build rules that image tag `least_electrification/latest` points to the same image hash as a canonical image tag
`least_electrification--debian/geonode/production/v2021.01.01`. This is useful for demo/quick-setup purposes so you can use shorter image name for brevity. 
However, keep in mind that image tag like `least_electrification/latest` is a moving target, so it's not intended for production deployment. Use canonical image tag
for production deployment and extending a base image tag.

If you need to build UI or CLI that leverages this image tag convention, consider using the following python regex:

```
^(?P<project_name>[\w-]+)--(?P<variant>[\w/]+)(/(?P<version>[v\d.]+))$
```

Both `project_name` and `version` uses the same sub regex and value type as described in the [git tag](#git-tag) section.

For `variant`, you can think of it like a value only filter (literal tags). It doesn't have hierarchical or ordering, but you can specify multiple values
to filter the image tag. `variant` is a slash separated values, or can be matched with regex `(\w+)` to return multiple groups match.

## Directory Structure

Root directory of the repository will consists for 3 main directories `build`, `src`, and `output`. `output` directory will always be ignored by git. `src` contains the source code or scripts. `build` contains a **generated** manifests that is ready to be build.

Files in the repository are arranged to allow for commit pulls from different branches. We uses overlays. Reasoning on why we are doing it like this:

- We avoid monorepo setup because we want to reuse and easily diff changes between build source from different external projects
- We manage multiple branches that tracks their own commit history for their respective project needs. These branches can evolve on their own.
- We want to be able to pull useful commits, cross-branches. If project A have useful updates, and project B wants it, we can just pull from project A.
- Directories are arranged to support overlays, in order for files from different project to not conflicting with the current project.
- If a pull from different branch cause conflicts, always choose files made in the current branch (ignoring files in the pulled branch). We can do this because
  we are using overlays, and that means the files in the current branch is the priority.
- If we want to make a change into any other target branch from changes in the current branch, the only way to do this is via pull request. If the pull request
  have conflicted files, this is the only way that the target branch can select files in the current branch to be accepted in their branch. This is a much clearer
  intention.
- Other files in the root directory of the repo is either already exists or generated from `src` directories.
- `build` directories always contains files that are generated by `src`. You should not modify it directly. Since it's always generated, we only persist it in git 
  because it's useful to directly see the files for a quick lookup in Github/git repo. Not because it needs to be persisted and saved.
- It promotes independent history between branches. This is useful for projects that have different lifecycles. They can choose to do pull request whenever they
  are ready, instead of forcing upstream and downstream to be always in sync.
- We can share the same builder scripts across branches easily with minimal friction with the `src` input.
- You can fetch useful commit from more than one source branches. Usually we need this to fetch commits related with the builder scripts. For example, `main`
  branch can benefit from a generic builder scripts in `project-A` branch and `project-B` branch by pulling from both of them. If `project-B` decides that it needs 
  commits from `project-A` it can pull directly from `project-A` or pull from `main` because it has `project-A` commits. All with minimal conflicts because the
  files are arranged as overlays.
  
## Source Overlays

`src` directories adopt overlays organizations.

`src` may contain one or more directories, but you can only directly manage one. If the current branch is A, then you can only directly manage subdir A. Any other dir exists because you are pulling from other branch. You are not allowed to change files in any other subdir, **except** when doing a PR. We call this subdir 
from now on as **overlay**.

If you branch out from existing branch A, into a new branch B, then you need to create a new subdir called B. You manage your files in subdir B. If the files you want to edit exists in subdir A, then copy that files over to subdir B and edit in this subdir. Now we have overlay A and overlay B. Overlays have certain ordering. Since B branches out from A, then we say overlay B have more `depth` value, or equivalently we can say that B is an overlay on top of A.

Each subdir in `src` must have a `source_config.yaml` as metadata. This metadata can be used by builder scripts to understand the overlays directory of `src`. See [source config](#source-config) for more info.

Overlays works by simple overrides. If overlay B have more `depth` value than overlay A, then whatever files/directories exists in B will overrides/overwrite files in A. These files will be generated and combined and be put in `build` directory. Files that only exists in A but not in B will exists in `build` directory.
Note that the file existence is merged, but not the content itself. So if a file called `Dockerfile` exists in A and B with different content, only B's 
`Dockerfile` content is used, completely overwriting whatever A's `Dockerfile` is.

### Special subdirectories and files inside an overlay

Some subdir and files inside the the overlay itself have specific uses in this repository.

#### source_config.yaml

A metadata file of the current overlay. It must exists so we know how to arrange these overlays. See [source config](#source-config)

#### build.sh

The build script. This file will be put in the `build` directory and can be run from there to run a build to produce output. 

File access in this script must assumes that it runs on a merged overlays, which is the `build` directory, and produce output into the `output` directory.

#### generator.sh

The generator script. This file will be put in the `build` directory and can be run from there to generate new files inside the `build` directory, befor the 
build happens.

File access in this script must assumes that it runs on a merged overlays and produce output, both from and to `build` directory.

#### rootfs

A directory used by docker builder. All the contents/files/dirs in `rootfs` directory are self contained. Which means it can only refer or linked to, files 
or directories inside rootfs itself.

`rootfs` gets copied by docker context. Dockerfile then can refer to it and put it inside the docker image with the `rootfs` mapped to `/` (root directory). 
For example, `rootfs/entrypoint.sh` will be copied to `/entrypoint.sh` inside the docker image.

#### .overlayignore

Any files or glob pattern included in this file as rows of patterns will be excluded from the final `build` directory of this overlay, and next overlay.

With overlays, it's easy to overwrite/replace files. However, to delete/exclude files from overlay below the current overlay, you need to declare it in this file to get processed.

Example, say overlay A contains a file called `base.html`. In overlay B, we want to exclude `base.html` from the final `build` directory. We do that by including
`base.html` in the `.overlayignore` file. The ignore only applies to current overlays. So if in overlay C, on top of overlay B, declares a new file `base.html`, the previous ignore file in overlay B doesn't apply.

### Source Config

Currently we define the following metadata (and sample values):

```yaml
# (string) project name. It should be the same as `src/{project_name}` name or git branch name with pattern `project-{project_name}`.
project_name: exciting
# (int) branch out level. How many times this source overlay have been branched from the `main` branch.
depth: 1
# `main` branch have depth: 0 . Branch that branches out from `main` have depth: 1 . If this is branches out again, increase the depth by 1.
dependencies:
  # Fill it with list of map that describes extra sources you need to build the output. Example below.
  # Each entry corresponds to the `src` subdir inside the current overlay. The content of the subdir comes from submodules to a specific commit/release.
  # For example, if we have gep component below, then from the root repository we have a directory `src/exciting/src/gep`
  - component_name: gep
    component_version: v1.0
  - component_name: mapstore
    component_version: v2020.12.01
# map that gets passed into the build phase
build_args:
# map that gets passed into the generator phase
generator_args:
```

## Phases

When performing a build. The following phases happens in the order they are written in this section:

### Bootstrap

No matter which branch we are working on, it will always have the `main` overlays, so we put our bootstrap scripts here under `src/main/bootstrap` directory. 
Bootstrap directory contains minimum files needed to bootstrap the build generator. Bootstrap script may write files or dirs to root directories, but it cannot 
edit other overlays.

Bootstrap phase can be used to create symlinks to files in root directories. This is useful if we want to create a file shortcut, like scripts or README docs.

### Overlays

In the overlays phase, we collect and merged files in `src` directories and put it there. This is a real copy and not a symlink. Symlink will also be copied as is.

### Generators

In the generators phase, we generate any files needed by the builders inside `build` directory. Some typical use case would be to concatenate multiple Dockerfile 
recipes to generate a single mult-stage Dockerfile recipe. Generators can also be used to generate config files from a template, like nginx config or uwsgi config.

### Builders

In the builders phase, we build the output and put it in `output` directory. In case of docker builders, we also push it to registry.

## Git Workflow

This section explains on how to utilize the project structure using Git workflow.

A single builder repo must always have one source branch, which is the `main` branch. We consider this the stable branch. Commits that goes here should 
be as generic as possible because it can be used by other branches. Commits that goes here should be the one that is guaranteed to work.

To extend from a branch, first you need to pick the source branch. As example, consider that we are going to create `develop` branch where we do some testing 
or create partial commits before it is merged to `main` branch. Checkout from the `main` branch to create the new branch called `develop`

```bash
# If using git checkout
git checkout main
git checkout -b develop

# If using git switch
git switch main -c develop 
```

In the new branch, create a new overlay directory `src/develop`. Then put all 
your overlays file there.
