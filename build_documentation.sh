#!/bin/bash 
namespace="NSAPH-Data-Platform"
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

git checkout "${doc_source_branch}"
if [ $? -ne 0 ]
then
  echo "Failed to checkout documentation branch: ${doc_source_branch}"
  exit 1
fi

git merge "${branch}"
if [ $? -ne 0 ]
then
  echo "Failed to merge latest changes into the documentation branch: ${doc_source_branch}"
  exit 1
fi


pip install -r doc-requirements.txt
pip install .
pip uninstall -y markupsafe
pip install markupsafe==2.0.1

rm -rf docs

# prepare rst templates for Python modules
collector  src/python doc/members

# prepare markdown templates for CWL files
cwl2md -i src/cwl -o doc/pipeline

# make python sources available for autodoc
abs_path=`realpath src/python`
export PATH="$abs_path:$PATH"

copy_section doc/utils.md doc/home.md dorieh.utils
copy_section doc/docutils.md doc/home.md dorieh.docutils
copy_section doc/platform.md doc/home.md dorieh.platform
copy_section doc/gis.md doc/home.md dorieh.gis
copy_section doc/AppPipelineGenerator.md doc/home.md dorieh.apppipelinegenerator
copy_section README.md doc/home.md readme

cp docker/README.md doc/docker_readme.md

# build documentation
sphinx-build doc docs || exit
touch docs/.nojekyll

echo "Build finished"

git add docs
git commit -a -m "Updating documentation"
echo "Changes committed"

echo Staging: "$staging"

if [ "${staging}" = "push" ]; then
  git push
elif [ "${staging}" != "" ]; then
  cp -R docs "${staging}"/
fi

git checkout "${branch}"
