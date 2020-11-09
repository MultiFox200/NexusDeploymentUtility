# Nexus Deployment Utility

Utility for automatic configuration of Nexus repositories, users, etc. </br>
Currently allow to automatically (parentheses contain json fields that are responsible for the feature):
- Change admin's password on first Nexus run; (prepare_admin_user)
- Enable\disable anonymous access; (anonymous_enabled)
- Create new users; (users)
- Delete default Nexus repositories (nuget-group, maven-snapshots, etc.); (remove_default_repositories)
- Create new repositories. (repositories)


## Usage
Firstly you need to to create `nexus.json` that will serve as configuration file for automatic configurations. For that you can use `nexus.json.sample` as example, it's configured to change admin's password, disable anonymous access, create one new user, remove default repositories and to create docker hosted and docket proxy repositories. For more possible repositories types you need to check `System/API` tab in Admin Settings of Nexus.

After setting up `nexus.json` you simply need to run `configure_run.sh` script that will apply all configured settings from `nexus.json` file.

If `configure_run.sh` was ran at least once you can use `run.sh` script instead.