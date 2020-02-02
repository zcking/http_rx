#!/usr/bin/env bash

# Parse branch name into <type>/<name>
branch_type=$(echo $TRAVIS_BRANCH | cut -d/ -f1)
branch_name=$(echo $TRAVIS_BRANCH | cut -d/ -f2)

# Parse the short commit hash
commit=$(git rev-parse --short HEAD)

case $branch_type in
  feature)
    version="$commit"
    ;;

  release)
    version="$branch_name.$TRAVIS_BUILD_NUMBER"
    echo "tagging release build $TRAVIS_COMMIT #$TRAVIS_BUILD_NUMBER with $branch_name"
    git tag -f $branch_name
    git push --tags
    ;;

  develop)
    version="$branch_name-$commit"
    ;;
  
  master)
    # Tag the commit and push the tags
    version=$(git tag --sort=committerdate --list '[0-9]*')
    echo "tagging master build $TRAVIS_COMMIT with $version"
    git tag -f $version $TRAVIS_COMMIT
    git push --tags
    ;;
  
  *)
    echo "unsupported branch type: $branch_type"
    version="$commit"
    ;;
esac

# Replace version in setup.py file for building
sed -i -E "s/version='.*',/version='$version',/" setup.py

