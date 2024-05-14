#!/bin/bash 

read -r -d '' help_text <<- EOM
Usage:
  -b - specify custom branch to clone. Default is 'main'
  -n - custom namespace on github to clone from. Default is 'NSAPH-Data-Platform'
EOM

namespace="NSAPH-Data-Platform"

dot -V
if [ $? -ne 0 ]
then
  echo "Graphviz `dot` utility is required to build this documentation. Please install: https://graphviz.org/download/"
  exit 1
fi

while getopts b:n: flag
do
    case "${flag}" in
        b) branch=${OPTARG};;
        n) namespace=${OPTARG};;
        *) echo "$help_text"; exit;;
    esac
done

rm -rf docs


for name in "${packages[@]}"
do
  package="${package_prefix}${name}"

  git clone --branch $branch https://github.com/$namespace/$package doc/common/$name

  # install library with dependencies
  if [ -a doc/common/$name/setup.py ]
  then
    pip install doc/common/$name
  fi

  # install dependencies if exists
  if [ -a doc/common/$name/requirements.txt ]
  then
    pip install -r doc/common/$name/requirements.txt
  fi

  # prepare rst templates for Python modules
  if [ -d doc/common/$name/src/python ]
  then
     collector doc/common/$name/src/python doc/common/$name/doc/members
  fi
  if [ "$name" = "utils" ]
  then
     collector doc/common/$name doc/common/$name/doc/members
  fi

  # prepare markdown templates for CWL files
  if [ -d doc/common/$name/src/cwl ]
  then
     mkdir -p doc/common/$name/doc/pipeline
     cwl2md -i doc/common/$name/src/cwl -o doc/common/$name/doc/pipeline
  fi

  # make python sources available for autodoc
  abs_path=`realpath doc/common/$name/src/python`
  if [ -n "$abs_path" ]
  then
    export PATH="$abs_path:$PATH"
  fi

done

copy_section doc/common/utils/README.md doc/home.md nsaph_utils
copy_section doc/common/core-platform/README.md doc/home.md nsaph
copy_section doc/common/gis/README.md doc/home.md gis


# build documentation
sphinx-build doc docs || exit
touch docs/.nojekyll

# remove copied repos
# rm -rf doc/common
git add docs
