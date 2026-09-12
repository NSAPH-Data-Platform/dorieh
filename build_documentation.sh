#!/bin/bash 
namespace="ForomePlatform"
doc_source_branch="doc-builder"
branch="main"


read -r -d '' help_text <<- EOM
Usage:
  -b - specify custom branch to clone. Default is ${branch}
  -n - custom namespace on github to clone from. Default is ${namespace}
  -s - staging documentation.
EOM


dot -V
if [ $? -ne 0 ]
then
  echo "Graphviz `dot` utility is required to build this documentation. Please install: https://graphviz.org/download/"
  exit 1
fi

staging=""

while getopts b:n:s: flag
do
    case "${flag}" in
        b) branch=${OPTARG};;
        n) namespace=${OPTARG};;
        s) staging=${OPTARG};;
        *) echo "$help_text"; exit;;
    esac
done

# Remember where we started; whatever happens below, finish there.
# The EXIT trap also guarantees that a failed merge never leaves the
# repository with unmerged paths: it is aborted before we leave.
original_ref="$(git symbolic-ref --quiet --short HEAD || git rev-parse HEAD)"
merge_started=0

cleanup() {
  rc=$?
  trap - EXIT
  if [ "${merge_started}" -eq 1 ] && \
     [ -e "$(git rev-parse --git-dir)/MERGE_HEAD" ]
  then
    git merge --abort || true
  fi
  current_ref="$(git symbolic-ref --quiet --short HEAD || git rev-parse HEAD)"
  if [ "${current_ref}" != "${original_ref}" ]
  then
    # We are mid-build on ${doc_source_branch}; anything dirty here is
    # build debris (the clean-tree guard ensured we started clean), so it
    # is safe to discard before returning to the original branch.
    git reset --hard --quiet || true
    git checkout "${original_ref}" || true
  fi
  exit ${rc}
}
trap cleanup EXIT

# This script switches branches (${doc_source_branch} and back), so
# uncommitted changes would travel across branches, and anything staged
# would be swept into the documentation commit. Untracked files under doc/
# are how machine-specific generated pages ended up committed on
# development branches in the past. Refuse to start in either situation
# (untracked files elsewhere are harmless and are left alone).
tracked_changes="$(git status --porcelain | grep -v '^?? ')"
doc_debris="$(git status --porcelain -- doc/ | grep '^?? ')"
if [ -n "${tracked_changes}" ] || [ -n "${doc_debris}" ]
then
  echo "Refusing to build documentation:"
  if [ -n "${tracked_changes}" ]
  then
    echo "- uncommitted changes to tracked files (commit or stash them first):"
    echo "${tracked_changes}" | head -20
  fi
  if [ -n "${doc_debris}" ]
  then
    echo "- untracked files under doc/ (remove them, or add them to .gitignore"
    echo "  if they are generated):"
    echo "${doc_debris}" | head -20
  fi
  exit 1
fi

git checkout "${doc_source_branch}"
if [ $? -ne 0 ]
then
  echo "Failed to checkout documentation branch: ${doc_source_branch}"
  exit 1
fi

# A stale local ${doc_source_branch} makes the merge below conflict
# spuriously; bring it up to date with its remote first.
if git fetch origin "${doc_source_branch}"
then
  if ! git merge --ff-only "origin/${doc_source_branch}"
  then
    echo "Local ${doc_source_branch} has diverged from origin/${doc_source_branch}; reconcile them manually."
    exit 1
  fi
else
  echo "WARNING: cannot fetch origin/${doc_source_branch}; building on the local state."
fi

merge_started=1
git merge "${branch}" -m "merging latest changes" --no-edit
if [ $? -ne 0 ]
then
  echo "Failed to merge ${branch} into the documentation branch: ${doc_source_branch}"
  exit 1
fi
merge_started=0


pip install -r doc-requirements.txt
pip install ".[FST]"
pip uninstall -y markupsafe
pip install markupsafe==2.0.1

rm -rf docs

# prepare rst templates for Python modules
collector  src/python doc/members

# prepare markdown templates for CWL files
cwl2md -i src/cwl -o doc/pipeline

# Purge stale generated files (ignored by git) left by earlier runs of the
# generators: a column or table removed from the model would otherwise leave
# its old page on disk, and Sphinx would build the orphan into the site
# (this is how pre-refactoring pages with machine-specific paths once
# reached the published docs). Everything removed here is regenerated below.
git clean -qfdX -- doc/lineage doc/tutorial/climate/mddocs

# generate the Medicare data dictionary and lineage pages (see doc/MedicareLineage.md).
# Must run from doc/lineage (the table/column lists are written to the CWD) and
# include both domain files, raw schemas first, so cross-domain lineage resolves.
(
  cd doc/lineage && \
  python -m dorieh.platform.dictionary.domain_dictionary \
      --fmt svg --lod min --mode sphinx -o medicare.dot \
      ../../src/python/dorieh/cms/models/medicare_cms.yaml \
      ../../src/python/dorieh/cms/models/medicare.yaml
) || { echo "Medicare lineage generation FAILED - refusing to build docs without it"; exit 1; }

# generate the climate tutorial data dictionary (doc/tutorial/climate/mddocs).
# Same policy as doc/lineage: these pages are generated at build time, not
# tracked; only the curated pages (example1.md, example1.png,
# example1cwl_src.md) and the book figure sources (table-lineage.dot, *.eps)
# are committed. Must run from the mddocs directory (the table/column lists
# are written to the CWD).
(
  cd doc/tutorial/climate/mddocs && \
  python -m dorieh.platform.dictionary.domain_dictionary \
      --fmt svg --lod min --mode sphinx -o example1.dot \
      ../example1_model.yml
) || { echo "Climate tutorial dictionary generation FAILED - refusing to build docs without it"; exit 1; }

# make python sources available for autodoc
abs_path=`realpath src/python`
export PATH="$abs_path:$PATH"

copy_section doc/utils.md doc/home.md dorieh.utils
copy_section doc/docutils.md doc/home.md dorieh.docutils
copy_section doc/platform.md doc/home.md dorieh.platform
copy_section doc/gis.md doc/home.md dorieh.gis
copy_section doc/AppPipelineGenerator.md doc/home.md dorieh.apppipelinegenerator
copy_section README.md doc/home.md readme

printf -- '---\norphan: true\n---\n\n' > doc/docker_readme.md
cat docker/README.md >> doc/docker_readme.md

# build documentation
sphinx-build -j auto doc docs || exit
# .doctrees is Sphinx's incremental-build cache: thousands of pickles that
# embed the builder machine's absolute paths. It must not be published.
rm -rf docs/.doctrees
touch docs/.nojekyll

echo "Build finished"

git add docs
# doc-builder is read-only for sources: discard the build-time mutations of
# tracked source files (copy_section injections into doc/home.md, the
# regenerated doc/docker_readme.md and doc/lineage artifacts), so that only
# the built site under docs/ is committed and merges from the dev branches
# can never conflict on generated content.
git checkout -- doc/
git commit -m "Updating documentation"
echo "Changes committed"

echo Staging: "$staging"

if [ "${staging}" = "push" ]; then
  git push
elif [ "${staging}" != "" ]; then
  # Replace, never accumulate: a page removed from the site must not
  # survive from an earlier build in the staging copy.
  rm -rf "${staging:?}/docs"
  cp -R docs "${staging}"/
fi

# Returning to the original branch is handled by the EXIT trap.
