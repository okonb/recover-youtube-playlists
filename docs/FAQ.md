# FAQ

### Why are the duration and thumbnail for some of my videos Unknown?
They probably were some of those impossibly long livestreams, and YouTube just doesn't keep this information for them.

### How does the script know which extractor to use?
Currently an extractor is chosen depending on creation date of your HTML file. This allows you to conveniently extract data from files you've saved long into the future. When that's not working for you, you can always try other extractors using the `--extractor` option.

### Why can't I commit?
Before each commit, a `pre-commit` git hook is invoked and a lint/test script runs. If the changes you've made prevent the script from running successfully, git will prevent you from completing a commit. If you want to commit anyway, run with the `--no-verify` option. Just remember to make sure that you don't push without verifying.