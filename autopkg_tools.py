#!/usr/bin/env python3

import subprocess
import git
import plistlib
import os

repo = git.Repo('munki_repo')

existing_branches = [ x.name[7:] for x in repo.remote().refs ]

print(existing_branches)
recipes = ['GoogleChromePkg.munki.recipe']

for recipe in recipes:
    output = '/tmp/autopkg.plist'
    cmd = f'/usr/local/bin/autopkg run overrides/{recipe} -v -q --report-plist {output}'
    subprocess.check_call(cmd, shell=True)

    with open(output, "rb") as f:
        report_data = plistlib.load(f)

    print(report_data)

    if 'summary_results' in report_data:
        package_name = report_data['summary_results']['munki_importer_summary_result']['data_rows'][0]['name']
        package_version = report_data['summary_results']['munki_importer_summary_result']['data_rows'][0]['version']
        package_info = report_data['summary_results']['munki_importer_summary_result']['data_rows'][0]['pkginfo_path']

        branch = f'{package_name}-{package_version}'

        if branch not in existing_branches:
            current = repo.create_head(branch)
            current.checkout()

            repo.git.add('pkgsinfo/' + package_info)
            repo.git.commit(m=f'Updated {package_name} to {package_version}')

            repo.git.push("origin", branch)
        else:
            print("not running because branch/pr already exists")

    repo.git.reset('--hard','origin/main')
    repo.heads.main.checkout()

    if os.path.exists(output):
        os.remove(output)
