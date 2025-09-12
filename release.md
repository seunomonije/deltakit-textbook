# Textbook Release Procedure

We currently have a fairly light-weight release process. At a high level, the docs are released by building the HTML content and uploading it to an Azure Blob Storage from which it will be used by our web application to serve on the Riverlane website. As the Textbook content and software stack matures, we will update this release process to include release notes, tests, and other continuous integration & deployment features.

These are the steps to releasing the Textbook:

1. The release manager checks out the commit to be released (typically the latest `main`), creates a tag (e.g. `git tag v0.1.0`), and pushes the tag to GitHub (`git push origin v0.1.0`).

1. The release manager triggers the stable release workflow on the tagged commit
   ("Build and publish Textbook" on GitHub Actions,
   [`release.yml`](https://github.com/deltakit/deltakit-textbook/blob/main/.github/workflows/release.yml)).
   This builds and uploads the artifacts to Azure Blob Storage.

1. The release manager pushes a new release of the web app to Staging for testing, and Prod upon release.
