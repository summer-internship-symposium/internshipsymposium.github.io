# internshipsymposium.github.io

This repository:
* Stores HTML/CSS/images for the UC San Diego CSE Summer Internship Symposium website
* Automatically deploys to [https://summer-internship-symposium.github.io/internshipsymposium.github.io/](https://summer-internship-symposium.github.io/internshipsymposium.github.io/) on commit and push to the repository
* Can be *manually* deployed to [https://internshipsymposium.ucsd.edu](https://internshipsymposium.ucsd.edu) by using Actions -> Deploy to internshipsymposium.ucsd.edu -> Run Workflow (from main branch)

## Editing
You can edit the HTML/CSS/images directly through the Github editing interfaces. When you commit/save, you will be able to see your changes reflected in [https://summer-internship-symposium.github.io/internshipsymposium.github.io/](https://summer-internship-symposium.github.io/internshipsymposium.github.io/) a few minutes later. It's also fine to clone and edit locally and push later, but for quick updates the web interface on Github is particularly convenient, especially if the goal is to just fix up some typos, etc.

The site is completely built in HTML and CSS, and there is no build system – it's just the files you see. As more pages get added it may be worth adding a build system to share a common header, etc. The Bootstrap CSS library is directly copied/hosted in the repository, which is the main exernal dependency for layout.

The [Bootstrap](https://getbootstrap.com/docs/4.0/) elements that are used are: grid (rows and columns), nav, and carousel. The media queries in symposium.css are designed around specific widths for the title.

## Deploying
The script in [.github/workflows](.github/workflows) is responsible for copying the files to [https://internshipsymposium.ucsd.edu](https://internshipsymposium.ucsd.edu) when we trigger the action. It has a SSH key for the pace user stored as a repository secret, and uses scp to copy and overwrite all the files in the relevant target directory on that host.

### Understanding [.github/workflows/main.yml](.github/workflows/main.yml): 
The environment variables are set so that files can be copied to the internshipsymposium.ucsd.edu server automatically
(without entering the password each time). To set this up, a public/private rsa key pair is needed.
1. Locally (e.g. in Terminal), run `ssh-keygen` and (when prompted) enter full path for file to save key
e.g. `/Users/username/.ssh/sis_rsa` 
and do not enter a passphrase (so that action can run without user input)
2. 

To deploy, use the Actions interface:


