import sys
import json
import os.path
import requests

f = open(sys.argv[1])
env = json.loads(f.read())
f.close()


def callNexusApi(method, url, data={}, headers={}, auth=None) -> requests.Response:
    base_url = env['base_url'] + 'v1/'
    auth = auth if auth else ('admin', env['admin_password'])

    with requests.Session() as session:
        if type(data) == dict:
            request = requests.Request(method=method, url=base_url + url, json=data, headers=headers, auth=auth)
        else:
            request = requests.Request(method=method, url=base_url + url, data=data, headers=headers, auth=auth)
        prepared_request = request.prepare()

        settings = session.merge_environment_settings(prepared_request.url, {}, None, None, None)
        response = session.send(prepared_request, **settings)
        response.raise_for_status()
        return response


def checkAdmin():
    admin_password_filepath = '/nexus-data/admin.password'
    if (os.path.isfile(admin_password_filepath)):
        f = open(admin_password_filepath)
        admin_password = f.read()
        f.close()

        callNexusApi(
            'PUT', 'security/users/admin/change-password',
            data=env['admin_password'],
            auth=('admin', admin_password),
            headers={'content-type': 'text/plain'}
        )


def setAnonymous():
    callNexusApi('PUT', 'security/anonymous', data={'enabled': env['anonymous_enabled']})


def checkUsers():
    users_to_create = env['users']
    users = callNexusApi('GET', 'security/users').json()

    for user in users_to_create:
        exists = bool(next(filter(lambda u: u['userId'] == user['userId'], users), False))
        if not exists:
            print(f"User {user['userId']} does not exists, creating")
            callNexusApi('POST', 'security/users', data={
                'status': 'active',
                **user
            })
        else:
            print(f"User {user['userId']} alredy exists, skipping")


def checkRepositories():
    repositories = callNexusApi('GET', 'repositories').json()

    if env['remove_default_repositories']:
        repositories_to_delete = ['nuget-group', 'maven-snapshots', 'nuget.org-proxy', 'maven-releases', 'nuget-hosted', 'maven-public', 'maven-central']

        existing_repositories_to_delete = [r for r in repositories if r['name'] in repositories_to_delete]

        for repository in existing_repositories_to_delete:
            delete_status = callNexusApi('DELETE', f'repositories/{repository["name"]}')
            if delete_status.status_code != 204:
                print(f"Couldn't delete repository '{repository['name']}' ({delete_status.status_code}: {delete_status.reason})")
            else:
                print(f"Removed repository '{repository['name']}'")

    repositories_to_create = env['repositories']

    repositories_names = [r['name'] for r in repositories]
    missing_repositories = [r for r in repositories_to_create if r['name'] not in repositories_names]

    for repository in missing_repositories:
        repo_type = repository.pop('type')
        callNexusApi('POST', f'repositories/{repo_type}', {'online': True, **repository})


def main():
    checkAdmin()
    setAnonymous()
    checkUsers()
    checkRepositories()


if __name__ == "__main__":
    main()